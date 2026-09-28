"""Authenticated browser commands for the Discover panel."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.components import websocket_api as ws
from homeassistant.core import HomeAssistant, callback

from .const import DOMAIN
from .discovery import DiscoveryError, RecipeDiscovery


def _service(hass: HomeAssistant) -> RecipeDiscovery:
    return next(iter(hass.data[DOMAIN].values()))


@callback
def async_register(hass: HomeAssistant) -> None:
    if hass.data.get(f"{DOMAIN}_ws_registered"):
        return
    hass.data[f"{DOMAIN}_ws_registered"] = True
    for handler in (state, search, import_recipe):
        ws.async_register_command(hass, handler)


@ws.websocket_command({vol.Required("type"): f"{DOMAIN}/state"})
@ws.async_response
async def state(hass: HomeAssistant, connection: ws.ActiveConnection, msg: dict) -> None:
    connection.send_result(msg["id"], {"providers": _service(hass).providers})


@ws.websocket_command({vol.Required("type"): f"{DOMAIN}/search", vol.Required("query"): vol.All(str, vol.Length(min=2, max=120)), vol.Required("provider"): vol.In(("web", "youtube"))})
@ws.async_response
async def search(hass: HomeAssistant, connection: ws.ActiveConnection, msg: dict) -> None:
    try:
        connection.send_result(msg["id"], await _service(hass).search(msg["query"], msg["provider"]))
    except DiscoveryError as exc:
        connection.send_error(msg["id"], "search_failed", str(exc))


@ws.websocket_command({vol.Required("type"): f"{DOMAIN}/import", vol.Required("url"): str})
@ws.async_response
async def import_recipe(hass: HomeAssistant, connection: ws.ActiveConnection, msg: dict) -> None:
    try:
        connection.send_result(msg["id"], {"url": await _service(hass).import_url(msg["url"])})
    except DiscoveryError as exc:
        connection.send_error(msg["id"], "import_failed", str(exc))
