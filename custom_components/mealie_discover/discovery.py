"""Search providers and Mealie API access, all from the Home Assistant server."""

from __future__ import annotations

import asyncio
from collections.abc import Mapping
from urllib.parse import quote, urlsplit

from aiohttp import ClientError, ClientResponseError, ClientSession

from .const import (
    CONF_GOOGLE_CX,
    CONF_GOOGLE_KEY,
    CONF_MEALIE_TOKEN,
    CONF_MEALIE_URL,
    CONF_YOUTUBE_KEY,
)


class DiscoveryError(Exception):
    """A provider or importer returned an actionable failure."""


class RecipeDiscovery:
    """Keep API keys server side and import only a result from a prior search."""

    def __init__(self, session: ClientSession, config: Mapping[str, str]) -> None:
        self.session = session
        self.config = config
        self.allowed: dict[str, str] = {}

    @property
    def providers(self) -> list[str]:
        result = []
        if self.config.get(CONF_GOOGLE_KEY):
            result.append("web")
        if self.config.get(CONF_YOUTUBE_KEY):
            result.append("youtube")
        return result

    async def _json(self, url: str, *, params=None, headers=None):
        try:
            async with asyncio.timeout(20):
                async with self.session.get(url, params=params, headers=headers) as response:
                    response.raise_for_status()
                    return await response.json()
        except (TimeoutError, ClientError, ValueError) as exc:
            raise DiscoveryError("Търсенето не успя. Провери API ключа, квотата и връзката.") from exc

    async def search(self, query: str, provider: str) -> list[dict]:
        if provider not in self.providers:
            raise DiscoveryError("Този източник не е настроен.")
        if provider == "youtube":
            results = await self._youtube(query)
        else:
            results = await self._web(query)
        # URL is never accepted for import unless it was returned by a provider.
        self.allowed = {item["url"]: item["provider"] for item in results}
        return results

    async def _web(self, query: str) -> list[dict]:
        response = await self._json(
            "https://customsearch.googleapis.com/customsearch/v1",
            params={
                "key": self.config[CONF_GOOGLE_KEY],
                "cx": self.config[CONF_GOOGLE_CX],
                "q": query + " рецепта",
                "num": 10,
                "gl": "bg",
            },
        )
        items = []
        for row in response.get("items", []):
            url = row.get("link", "")
            if urlsplit(url).scheme != "https":
                continue
            metatags = (row.get("pagemap", {}).get("metatags") or [{}])[0]
            rating = next(iter(row.get("pagemap", {}).get("aggregaterating", [])), {})
            items.append({
                "title": row.get("title", "Recipe"),
                "url": url,
                "provider": "web",
                "source": urlsplit(url).hostname,
                "description": row.get("snippet", ""),
                "image": metatags.get("og:image", ""),
                "rating": rating.get("ratingvalue"),
                "rating_count": rating.get("ratingcount") or rating.get("reviewcount"),
            })
        return items

    async def _youtube(self, query: str) -> list[dict]:
        key = self.config[CONF_YOUTUBE_KEY]
        found = await self._json(
            "https://www.googleapis.com/youtube/v3/search",
            params={"part": "snippet", "type": "video", "order": "viewCount", "q": query + " рецепта", "maxResults": 20, "key": key},
        )
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
                "views": int(counts.get(video_id, {}).get("viewCount", 0)),
                "likes": int(counts.get(video_id, {}).get("likeCount", 0)),
            })
        return sorted(result, key=lambda item: item["views"], reverse=True)

    async def import_url(self, url: str) -> str:
        if url not in self.allowed:
            raise DiscoveryError("Първо потърси и избери рецепта от резултатите.")
        try:
            async with asyncio.timeout(90):
                async with self.session.post(
                    f"{self.config[CONF_MEALIE_URL]}/api/recipes/create/url",
                    json={"url": url},
                    headers={"Authorization": f"Bearer {self.config[CONF_MEALIE_TOKEN]}"},
                ) as response:
                    response.raise_for_status()
                    slug = await response.json()
        except (TimeoutError, ClientResponseError, ClientError, ValueError) as exc:
            raise DiscoveryError("Mealie не успя да импортира адреса. Провери API токена и дали сайтът се поддържа. За видео може да е необходим AI importer в Mealie.") from exc
        if not isinstance(slug, str) or not slug:
            raise DiscoveryError("Mealie не върна адрес на новата рецепта.")
        self.allowed.pop(url, None)
        return f"{self.config[CONF_MEALIE_URL]}/g/home/r/{quote(slug, safe='')}"
