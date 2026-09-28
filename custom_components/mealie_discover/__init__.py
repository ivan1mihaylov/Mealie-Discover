"""Find public recipes and send selected URLs to Mealie."""

from __future__ import annotations

from pathlib import Path

from homeassistant.components.frontend import async_remove_panel
from homeassistant.components.http import StaticPathConfig
from homeassistant.components.panel_custom import async_register_panel
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType
from homeassistant.loader import async_get_integration

from .const import DOMAIN
from .discovery import RecipeDiscovery
from .websocket_api import async_register

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

_PANEL_PATH = "mealie-discover"
_SCRIPT_URL = "/mealie_discover/panel.js"

type MealieDiscoverConfigEntry = ConfigEntry[RecipeDiscovery]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Register the static script and WebSocket commands once per Home Assistant run."""
    await hass.http.async_register_static_paths(
        [StaticPathConfig(_SCRIPT_URL, str(Path(__file__).parent / "panel.js"), False)]
    )
    async_register(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: MealieDiscoverConfigEntry) -> bool:
    """Expose a sidebar panel backed by authenticated WebSocket commands."""
    entry.runtime_data = RecipeDiscovery(async_get_clientsession(hass), entry.data)
    integration = await async_get_integration(hass, DOMAIN)
    await async_register_panel(
        hass,
        frontend_url_path=_PANEL_PATH,
        webcomponent_name="mealie-discover-panel",
        sidebar_title="Mealie Discover",
        sidebar_icon="mdi:food-search",
        # The version busts the browser cache after an update from HACS.
        module_url=f"{_SCRIPT_URL}?v={integration.version}",
        config_panel_domain=DOMAIN,
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: MealieDiscoverConfigEntry) -> bool:
    """Remove the panel when the integration is removed or reloaded."""
    async_remove_panel(hass, _PANEL_PATH)
    return True
