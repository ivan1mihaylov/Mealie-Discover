"""Search providers and Mealie API access, all from the Home Assistant server."""

from __future__ import annotations

import asyncio
from collections import OrderedDict
from collections.abc import Mapping
import ipaddress
import json
import logging
import re
from typing import Any
from urllib.parse import quote, urlsplit

from aiohttp import ClientError, ClientResponse, ClientSession

from .const import CONF_MEALIE_TOKEN, CONF_MEALIE_URL, CONF_SEARXNG_URL, CONF_YOUTUBE_KEY

_LOGGER = logging.getLogger(__name__)

# Import is allowed only for URLs a search returned; keep enough for several tabs.
_ALLOWED_LIMIT = 200
_WEB_RESULTS = 12
# Bytes read from a result page while looking for its schema.org Recipe.
_PAGE_LIMIT = 2_000_000
_PAGE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; MealieDiscover; +https://github.com/ivan1mihaylov/Mealie-Discover)",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "bg,en;q=0.8",
}
_LD_JSON = re.compile(
    r"<script[^>]*type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>", re.I | re.S
)
_CYRILLIC = re.compile(r"[\u0400-\u04FF]")
_RECIPE_WORD = re.compile(r"рецепт|recipe", re.I)
LANGUAGES = ("all", "bg", "en")
_DURATION = re.compile(r"^P(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:[\d.]+S)?)?$", re.I)


class DiscoveryError(Exception):
    """A provider or importer returned an actionable failure."""

    def __init__(self, message: str, code: str = "failed") -> None:
        super().__init__(message)
        self.code = code


class RecipeDiscovery:
    """Keep API keys server side and import only a result from a prior search."""

    def __init__(self, session: ClientSession, config: Mapping[str, Any]) -> None:
        self.session = session
        self.config = config
        self.allowed: OrderedDict[str, str] = OrderedDict()
        self._group_slug: str | None = None

    @property
    def providers(self) -> list[str]:
        result = []
        if self.config.get(CONF_SEARXNG_URL):
            result.append("web")
        if self.config.get(CONF_YOUTUBE_KEY):
            result.append("youtube")
        return result

    @property
    def _mealie_url(self) -> str:
        return self.config[CONF_MEALIE_URL]

    @property
    def _mealie_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.config[CONF_MEALIE_TOKEN]}"}

    async def _json(self, url: str, *, params=None, headers=None):
        try:
            async with asyncio.timeout(20):
                async with self.session.get(url, params=params, headers=headers) as response:
                    response.raise_for_status()
                    return await response.json(content_type=None)
        except (TimeoutError, ClientError, ValueError) as exc:
            raise DiscoveryError("Търсенето не успя. Провери настройките, квотата и връзката.") from exc

    async def check_mealie(self) -> None:
        """Verify the URL and token with a cheap authenticated call."""
        try:
            async with asyncio.timeout(15):
                async with self.session.get(
                    f"{self._mealie_url}/api/users/self", headers=self._mealie_headers
                ) as response:
                    if response.status in (401, 403):
                        raise DiscoveryError("Invalid Mealie token", "invalid_auth")
                    response.raise_for_status()
                    user = await response.json()
        except (TimeoutError, ClientError, ValueError) as exc:
            raise DiscoveryError("Mealie is unreachable", "cannot_connect") from exc
        self._group_slug = _group_slug(user)

    async def check_searxng(self) -> None:
        """Verify SearXNG answers with its JSON output format enabled."""
        try:
            async with asyncio.timeout(20):
                async with self.session.get(
                    f"{self.config[CONF_SEARXNG_URL]}/search",
                    params={"q": "рецепта", "format": "json"},
                ) as response:
                    if response.status == 403:
                        raise DiscoveryError("SearXNG JSON format is disabled", "searxng_json")
                    response.raise_for_status()
                    body = await response.json(content_type=None)
        except (TimeoutError, ClientError, ValueError) as exc:
            raise DiscoveryError("SearXNG is unreachable", "searxng_unreachable") from exc
        if not isinstance(body, dict) or "results" not in body:
            raise DiscoveryError("SearXNG returned no results list", "searxng_unreachable")

    async def search(self, query: str, provider: str, language: str = "all") -> list[dict]:
        if provider not in self.providers:
            raise DiscoveryError("Този източник не е настроен.")
        query = _recipe_query(query)
        if provider == "youtube":
            results = await self._youtube(query, language)
        else:
            results = await self._web(query, language)
        # URL is never accepted for import unless it was returned by a provider.
        for item in results:
            self.allowed[item["url"]] = item["provider"]
            self.allowed.move_to_end(item["url"])
        while len(self.allowed) > _ALLOWED_LIMIT:
            self.allowed.popitem(last=False)
        return results

    async def _web(self, query: str, language: str) -> list[dict]:
        response = await self._json(
            f"{self.config[CONF_SEARXNG_URL]}/search",
            params={
                "q": query,
                "format": "json",
                "language": language,
                "categories": "general",
                "safesearch": 1,
            },
        )
        items: list[dict] = []
        seen: set[str] = set()
        for row in response.get("results", []):
            url = row.get("url") or ""
            if url in seen or not _public_https(url):
                continue
            seen.add(url)
            image = row.get("img_src") or row.get("thumbnail") or ""
            items.append({
                "title": row.get("title") or "Recipe",
                "url": url,
                "provider": "web",
                "source": urlsplit(url).hostname,
                "description": row.get("content") or "",
                "image": image if _public_https(image) else "",
                "is_recipe": False,
                "rating": None,
                "rating_count": None,
                "total_minutes": None,
            })
            if len(items) >= _WEB_RESULTS:
                break
        await asyncio.gather(*(self._enrich(item) for item in items))
        # Pages with a schema.org Recipe come first (Mealie can import those),
        # then the most rated; ties keep the search engine's order.
        items.sort(key=lambda item: (not item["is_recipe"], -(item["rating_count"] or 0)))
        return items

    async def _enrich(self, item: dict) -> None:
        """Read rating and cooking time from the page's schema.org Recipe."""
        try:
            async with asyncio.timeout(10):
                async with self.session.get(item["url"], headers=_PAGE_HEADERS) as response:
                    if response.status != 200 or "html" not in response.content_type:
                        return
                    if not _public_https(str(response.url)):
                        return
                    raw = await response.content.read(_PAGE_LIMIT)
                    charset = response.charset or "utf-8"
        except (TimeoutError, ClientError):
            return
        try:
            html = raw.decode(charset, "replace")
        except LookupError:
            html = raw.decode("utf-8", "replace")
        recipe = _find_recipe(html)
        if recipe is None:
            return
        item["is_recipe"] = True
        rating = recipe.get("aggregateRating")
        if isinstance(rating, list):
            rating = rating[0] if rating else None
        if isinstance(rating, dict):
            item["rating"] = _number(rating.get("ratingValue"))
            item["rating_count"] = _count(rating.get("ratingCount")) or _count(rating.get("reviewCount"))
        total = _minutes(recipe.get("totalTime"))
        if total is None:
            parts = [_minutes(recipe.get(key)) for key in ("prepTime", "cookTime")]
            total = sum(p for p in parts if p) or None
        item["total_minutes"] = total
        if not item["image"]:
            image = _image(recipe.get("image"))
            item["image"] = image if _public_https(image) else ""

    async def _youtube(self, query: str, language: str) -> list[dict]:
        key = self.config[CONF_YOUTUBE_KEY]
        params = {
            "part": "snippet",
            "type": "video",
            "order": "viewCount",
            "q": query,
            "maxResults": 20,
            "key": key,
        }
        if language != "all":
            params["relevanceLanguage"] = language
        if language == "bg":
            params["regionCode"] = "BG"
        found = await self._json("https://www.googleapis.com/youtube/v3/search", params=params)
        rows = found.get("items", [])
        ids = [row.get("id", {}).get("videoId") for row in rows]
        ids = [video_id for video_id in ids if video_id]
        if not ids:
            return []
        stats = await self._json(
            "https://www.googleapis.com/youtube/v3/videos",
            params={"part": "statistics", "id": ",".join(ids), "key": key},
        )
        counts = {row["id"]: row.get("statistics", {}) for row in stats.get("items", [])}
        result = []
        for row in rows:
            video_id = row.get("id", {}).get("videoId")
            if not video_id:
                continue
            snippet = row.get("snippet", {})
            thumbnails = snippet.get("thumbnails", {})
            result.append({
                "title": snippet.get("title", "Video"),
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "provider": "youtube",
                "source": snippet.get("channelTitle", "YouTube"),
                "description": snippet.get("description", ""),
                "image": (thumbnails.get("medium") or thumbnails.get("default") or {}).get("url", ""),
                "views": _count(counts.get(video_id, {}).get("viewCount")) or 0,
                "likes": _count(counts.get(video_id, {}).get("likeCount")) or 0,
            })
        return sorted(result, key=lambda item: item["views"], reverse=True)

    async def import_url(self, url: str) -> dict[str, str]:
        provider = self.allowed.get(url)
        if provider is None:
            raise DiscoveryError("Първо потърси и избери рецепта от резултатите.")
        try:
            async with asyncio.timeout(90):
                async with self.session.post(
                    f"{self._mealie_url}/api/recipes/create/url",
                    json={"url": url},
                    headers=self._mealie_headers,
                ) as response:
                    if response.status >= 400:
                        raise DiscoveryError(await _import_error(response, provider))
                    slug = await response.json(content_type=None)
        except (TimeoutError, ClientError, ValueError) as exc:
            raise DiscoveryError("Mealie не отговори. Провери адреса на Mealie и връзката от Home Assistant.") from exc
        if not isinstance(slug, str) or not slug:
            raise DiscoveryError("Mealie не върна адрес на новата рецепта.")
        self.allowed.pop(url, None)
        linked, total = await self._link_ingredients(slug)
        path = f"/g/{quote(await self._group(), safe='')}/r/{quote(slug, safe='')}"
        return {"url": self._mealie_url + path, "path": path, "linked": linked, "total": total}

    async def _mealie(self, method: str, path: str, *, json: Any = None, timeout: int = 30) -> Any:
        async with asyncio.timeout(timeout):
            async with self.session.request(
                method, f"{self._mealie_url}{path}", json=json, headers=self._mealie_headers
            ) as response:
                response.raise_for_status()
                return await response.json(content_type=None)

    async def _link_ingredients(self, slug: str) -> tuple[int, int]:
        """Parse the imported text ingredients and link them to existing foods and units.

        Mealie stores URL imports as plain text; its parser matches existing foods
        and units, with AI when OpenAI is configured. Lines whose food is not in
        Mealie stay as text so no duplicate foods are created. Failures keep the
        recipe as imported.
        """
        try:
            recipe = await self._mealie("GET", f"/api/recipes/{quote(slug, safe='')}")
            ingredients = recipe.get("recipeIngredient") or []
            texts = [_ingredient_text(item) for item in ingredients]
            wanted = [text for text in texts if text]
            if not wanted:
                return 0, 0
            parsed = None
            for parser in ("openai", "brute"):
                try:
                    parsed = await self._mealie(
                        "POST", "/api/parser/ingredients",
                        json={"parser": parser, "ingredients": wanted}, timeout=120,
                    )
                except (TimeoutError, ClientError, ValueError):
                    continue
                if isinstance(parsed, list) and len(parsed) == len(wanted):
                    break
                parsed = None
            if parsed is None:
                return 0, len(wanted)
            results = iter(parsed)
            linked = 0
            updated = []
            for item, text in zip(ingredients, texts):
                if not text:
                    updated.append(item)
                    continue
                ingredient = _linked_ingredient(item, text, next(results))
                linked += ingredient is not item
                updated.append(ingredient)
            if linked:
                recipe["recipeIngredient"] = updated
                await self._mealie("PUT", f"/api/recipes/{quote(slug, safe='')}", json=recipe)
            return linked, len(wanted)
        except (TimeoutError, ClientError, ValueError, TypeError, AttributeError):
            _LOGGER.warning("Could not link the ingredients of %s", slug, exc_info=True)
            return 0, 0

    async def _group(self) -> str:
        """Mealie's recipe URLs contain the user's group slug."""
        if self._group_slug is None:
            try:
                user = await self._json(f"{self._mealie_url}/api/users/self", headers=self._mealie_headers)
            except DiscoveryError:
                return "home"
            self._group_slug = _group_slug(user)
        return self._group_slug


async def _import_error(response: ClientResponse, provider: str) -> str:
    if response.status in (401, 403):
        return "Mealie отказа достъп. Провери API токена."
    try:
        body = await response.json(content_type=None)
    except (ClientError, ValueError):
        body = None
    detail = body.get("detail") if isinstance(body, dict) else None
    if isinstance(detail, dict):
        detail = detail.get("message") or detail.get("error")
    elif isinstance(detail, list) and detail and isinstance(detail[0], dict):
        detail = detail[0].get("msg")
    message = "Mealie не успя да импортира рецептата"
    message += f": {detail}" if isinstance(detail, str) and detail else ". Възможно е сайтът да не се поддържа."
    if provider == "youtube":
        message += " За видео е необходим AI импорт (OpenAI) в Mealie."
    return message


def _ingredient_text(item: Any) -> str:
    """The original text of an unparsed ingredient; empty for linked ones and section headers."""
    if not isinstance(item, dict) or (item.get("food") or {}).get("id"):
        return ""
    for key in ("originalText", "note", "display"):
        if isinstance(item.get(key), str) and item[key].strip():
            return item[key].strip()
    return ""


def _linked_ingredient(item: dict, text: str, parsed: Any) -> dict:
    """Use the parser's result only when it found an existing food."""
    ingredient = parsed.get("ingredient") if isinstance(parsed, dict) else None
    food = (ingredient or {}).get("food") or {}
    if not food.get("id"):
        return item
    unit = ingredient.get("unit") or {}
    note = (ingredient.get("note") or "").strip()
    if unit and not unit.get("id"):
        # An unknown unit stays readable in the note instead of creating a new unit.
        note = f"{unit.get('name', '')} {note}".strip()
        unit = None
    return {
        **item,
        "quantity": ingredient.get("quantity") or 0,
        "unit": unit or None,
        "food": food,
        "note": note,
        "display": "",
        "originalText": text,
    }


def _recipe_query(query: str) -> str:
    """Add "recipe" in the query's alphabet unless the user already wrote it."""
    if _RECIPE_WORD.search(query):
        return query
    return f"{query} {'рецепта' if _CYRILLIC.search(query) else 'recipe'}"


def _group_slug(user: Any) -> str:
    slug = user.get("groupSlug") if isinstance(user, dict) else None
    return slug if isinstance(slug, str) and slug else "home"


def _public_https(url: str) -> bool:
    """Reject non-HTTPS links and links to local or private addresses."""
    parts = urlsplit(url or "")
    host = parts.hostname
    if parts.scheme != "https" or not host or host == "localhost" or host.endswith(".local"):
        return False
    try:
        return ipaddress.ip_address(host).is_global
    except ValueError:
        return True


def _find_recipe(html: str) -> dict | None:
    for block in _LD_JSON.findall(html):
        try:
            data = json.loads(block.strip())
        except ValueError:
            continue
        if recipe := _walk(data):
            return recipe
    return None


def _walk(node: Any) -> dict | None:
    if isinstance(node, list):
        for child in node:
            if recipe := _walk(child):
                return recipe
    elif isinstance(node, dict):
        kind = node.get("@type")
        if "Recipe" in (kind if isinstance(kind, list) else [kind]):
            return node
        for key in ("@graph", "mainEntity"):
            if recipe := _walk(node.get(key)):
                return recipe
    return None


def _number(value: Any) -> float | None:
    try:
        number = float(str(value).replace(",", ".").strip())
    except ValueError:
        return None
    return round(number, 1) if number > 0 else None


def _count(value: Any) -> int | None:
    digits = re.sub(r"\D", "", str(value)) if value is not None else ""
    return int(digits) if digits else None


def _minutes(value: Any) -> int | None:
    match = _DURATION.match(value.strip()) if isinstance(value, str) else None
    if not match or not any(match.groups()):
        return None
    days, hours, minutes = (int(group or 0) for group in match.groups())
    return days * 1440 + hours * 60 + minutes or None


def _image(value: Any) -> str:
    if isinstance(value, list):
        value = value[0] if value else ""
    if isinstance(value, dict):
        value = value.get("url") or ""
    return value if isinstance(value, str) else ""
