"""UI configuration for the recipe discovery integration."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlsplit

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_MEALIE_TOKEN,
    CONF_MEALIE_URL,
    CONF_SEARXNG_URL,
    CONF_SOCIAL_URL,
    CONF_YOUTUBE_KEY,
    DOMAIN,
)
from .addons import async_detect_urls
from .discovery import DiscoveryError, RecipeDiscovery


def _clean_url(value: str) -> str | None:
    url = value.strip().rstrip("/")
    parsed = urlsplit(url)
    if (
        parsed.scheme not in ("http", "https")
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
    ):
        return None
    return url


def _schema(defaults: dict[str, Any]) -> vol.Schema:
    def field(key: str) -> dict[str, Any]:
        return {"description": {"suggested_value": defaults.get(key)}}

    return vol.Schema(
        {
            vol.Required(CONF_MEALIE_URL, **field(CONF_MEALIE_URL)): str,
            vol.Required(CONF_MEALIE_TOKEN, **field(CONF_MEALIE_TOKEN)): str,
            vol.Optional(CONF_SEARXNG_URL, **field(CONF_SEARXNG_URL)): str,
            vol.Optional(CONF_YOUTUBE_KEY, **field(CONF_YOUTUBE_KEY)): str,
            vol.Optional(CONF_SOCIAL_URL, **field(CONF_SOCIAL_URL)): str,
        }
    )


class MealieDiscoverConfigFlow(ConfigFlow, domain=DOMAIN):
    """Set up a single Mealie connection and optional search providers."""

    VERSION = 1

    _detected: dict[str, str] | None = None

    async def _detect(self) -> dict[str, str]:
        """Look for SearXNG, Mealie and Social to Mealie add-ons once per flow."""
        if self._detected is None:
            self._detected = await async_detect_urls(self.hass)
        return self._detected

    def _placeholders(self) -> dict[str, str]:
        names = {CONF_SEARXNG_URL: "SearXNG", CONF_MEALIE_URL: "Mealie", CONF_SOCIAL_URL: "Social to Mealie"}
        found = [f"{names[key]}: {url}" for key, url in (self._detected or {}).items()]
        return {"detected": ", ".join(found) or "—"}

    async def _validate(self, user_input: dict[str, Any]) -> tuple[dict[str, Any], dict[str, str]]:
        """Normalize the form and check Mealie, SearXNG and Social to Mealie from Home Assistant."""
        errors: dict[str, str] = {}
        data = {
            CONF_MEALIE_URL: _clean_url(user_input[CONF_MEALIE_URL]),
            CONF_MEALIE_TOKEN: user_input[CONF_MEALIE_TOKEN].strip(),
        }
        if data[CONF_MEALIE_URL] is None:
            errors[CONF_MEALIE_URL] = "invalid_url"
        if searxng := (user_input.get(CONF_SEARXNG_URL) or "").strip():
            data[CONF_SEARXNG_URL] = _clean_url(searxng)
            if data[CONF_SEARXNG_URL] is None:
                errors[CONF_SEARXNG_URL] = "invalid_url"
        if youtube := (user_input.get(CONF_YOUTUBE_KEY) or "").strip():
            data[CONF_YOUTUBE_KEY] = youtube
        if social := (user_input.get(CONF_SOCIAL_URL) or "").strip():
            data[CONF_SOCIAL_URL] = _clean_url(social)
            if data[CONF_SOCIAL_URL] is None:
                errors[CONF_SOCIAL_URL] = "invalid_url"
        if not searxng and not youtube and not social:
            errors["base"] = "provider_required"
        if errors:
            return data, errors

        discovery = RecipeDiscovery(async_get_clientsession(self.hass), data)
        try:
            await discovery.check_mealie()
        except DiscoveryError as exc:
            errors["base"] = exc.code
            return data, errors
        if searxng:
            try:
                await discovery.check_searxng()
            except DiscoveryError as exc:
                errors[CONF_SEARXNG_URL] = exc.code
        if social:
            try:
                await discovery.check_social()
            except DiscoveryError as exc:
                errors[CONF_SOCIAL_URL] = exc.code
        return data, errors

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            data, errors = await self._validate(user_input)
            if not errors:
                await self.async_set_unique_id(DOMAIN)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title="Mealie Discover", data=data)
        detected = await self._detect()
        return self.async_show_form(
            step_id="user",
            data_schema=_schema(user_input or detected),
            errors=errors,
            description_placeholders=self._placeholders(),
        )

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Change the Mealie connection or search providers without re-adding."""
        entry = self._get_reconfigure_entry()
        errors: dict[str, str] = {}
        if user_input is not None:
            data, errors = await self._validate(user_input)
            if not errors:
                return self.async_update_reload_and_abort(entry, data=data)
        detected = await self._detect()
        current = {key: value for key, value in entry.data.items() if value}
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=_schema(user_input or {**detected, **current}),
            errors=errors,
            description_placeholders=self._placeholders(),
        )
