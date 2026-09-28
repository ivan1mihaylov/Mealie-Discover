"""UI configuration for the recipe discovery integration."""

from urllib.parse import urlsplit

import voluptuous as vol

from homeassistant import config_entries

from .const import (
    CONF_GOOGLE_CX,
    CONF_GOOGLE_KEY,
    CONF_MEALIE_TOKEN,
    CONF_MEALIE_URL,
    CONF_YOUTUBE_KEY,
    DOMAIN,
)


class MealieDiscoverConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Set up a single Mealie connection and optional search providers."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            url = user_input[CONF_MEALIE_URL].strip().rstrip("/")
            parsed = urlsplit(url)
            if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
                errors[CONF_MEALIE_URL] = "invalid_url"
            elif bool(user_input.get(CONF_GOOGLE_KEY)) != bool(user_input.get(CONF_GOOGLE_CX)):
                errors["base"] = "google_pair"
            elif not user_input.get(CONF_GOOGLE_KEY) and not user_input.get(CONF_YOUTUBE_KEY):
                errors["base"] = "provider_required"
            else:
                await self.async_set_unique_id("mealie_discover")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title="Mealie Discover", data={**user_input, CONF_MEALIE_URL: url}
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_MEALIE_URL): str,
                vol.Required(CONF_MEALIE_TOKEN): str,
                vol.Optional(CONF_GOOGLE_KEY): str,
                vol.Optional(CONF_GOOGLE_CX): str,
                vol.Optional(CONF_YOUTUBE_KEY): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
