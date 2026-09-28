"""Find public recipes and send selected URLs to Mealie."""

from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.components.http import StaticPathConfig
from homeassistant.components.panel_custom import async_register_panel
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .discovery import RecipeDiscovery
from .websocket_api import async_register

_LOGGER = logging.getLogger(__name__)
_PANEL_PATH = "mealie-discover"
_SCRIPT_URL = "/mealie_discover/panel.js"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Expose a sidebar panel backed by authenticated WebSocket commands."""
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = RecipeDiscovery(
        async_get_clientsession(hass), entry.data
    )
    await hass.http.async_register_static_paths(
        [StaticPathConfig(_SCRIPT_URL, str(Path(__file__).parent / "panel.js"), False)]
    )
    async_register(hass)
    await async_register_panel(
        hass,
        frontend_url_path=_PANEL_PATH,
        webcomponent_name="mealie-discover-panel",
        sidebar_title="Mealie Discover",
        sidebar_icon="mdi:food-search",
        module_url=_SCRIPT_URL,
        config_panel_domain=DOMAIN,
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Remove the panel when the integration is removed."""
    from homeassistant.components.frontend import async_remove_panel

    async_remove_panel(hass, _PANEL_PATH)
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True
