"""Authenticated browser commands for the Discover panel."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.components import websocket_api as ws
from homeassistant.core import HomeAssistant, callback

from .addons import async_mealie_panel
from .const import DOMAIN
from .discovery import LANGUAGES, DiscoveryError, RecipeDiscovery


def _service(hass: HomeAssistant) -> RecipeDiscovery:
    for entry in hass.config_entries.async_loaded_entries(DOMAIN):
        return entry.runtime_data
    raise DiscoveryError("Интеграцията Mealie Discover не е заредена.", "not_loaded")


@callback
def async_register(hass: HomeAssistant) -> None:
    for handler in (state, search, import_recipe, import_social, recipe):
        ws.async_register_command(hass, handler)


@ws.websocket_command({vol.Required("type"): f"{DOMAIN}/state"})
@ws.async_response
async def state(hass: HomeAssistant, connection: ws.ActiveConnection, msg: dict) -> None:
    try:
        service = _service(hass)
        connection.send_result(
            msg["id"],
            {
                "providers": service.providers,
                "social": service.social,
                "mealie_panel": await async_mealie_panel(hass),
            },
        )
    except DiscoveryError as exc:
        connection.send_error(msg["id"], exc.code, str(exc))


@ws.websocket_command({vol.Required("type"): f"{DOMAIN}/search", vol.Required("query"): vol.All(str, vol.Length(min=2, max=120)), vol.Required("provider"): vol.In(("web", "youtube")), vol.Optional("language", default="all"): vol.In(LANGUAGES)})
@ws.async_response
async def search(hass: HomeAssistant, connection: ws.ActiveConnection, msg: dict) -> None:
    try:
        connection.send_result(msg["id"], await _service(hass).search(msg["query"], msg["provider"], msg["language"]))
    except DiscoveryError as exc:
        connection.send_error(msg["id"], "search_failed", str(exc))


@ws.websocket_command({vol.Required("type"): f"{DOMAIN}/import", vol.Required("url"): str})
@ws.async_response
async def import_recipe(hass: HomeAssistant, connection: ws.ActiveConnection, msg: dict) -> None:
    try:
        connection.send_result(msg["id"], await _service(hass).import_url(msg["url"]))
    except DiscoveryError as exc:
        connection.send_error(msg["id"], "import_failed", str(exc))


@ws.websocket_command({vol.Required("type"): f"{DOMAIN}/import_social", vol.Required("url"): vol.All(str, vol.Length(min=8, max=2000))})
@ws.async_response
async def import_social(hass: HomeAssistant, connection: ws.ActiveConnection, msg: dict) -> None:
    try:
        connection.send_result(msg["id"], await _service(hass).import_social(msg["url"]))
    except DiscoveryError as exc:
        connection.send_error(msg["id"], "import_failed", str(exc))


@ws.websocket_command({vol.Required("type"): f"{DOMAIN}/recipe", vol.Required("slug"): vol.All(str, vol.Length(min=1, max=300))})
@ws.async_response
async def recipe(hass: HomeAssistant, connection: ws.ActiveConnection, msg: dict) -> None:
    try:
        connection.send_result(msg["id"], await _service(hass).recipe(msg["slug"]))
    except DiscoveryError as exc:
        connection.send_error(msg["id"], "recipe_failed", str(exc))
