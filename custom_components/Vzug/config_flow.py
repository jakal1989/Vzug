from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
import voluptuous as vol
import logging

# Logger für Debugging
_LOGGER = logging.getLogger(__name__)

# Definiere die Konfigurationsschema
DATA_SCHEMA = vol.Schema({
    vol.Required("dishwasher_ip"): str,
    vol.Required("oven_ip"): str,
})

class VzugConfigFlow(config_entries.ConfigFlow, domain="vzug"):
    """Handle a config flow for V-ZUG."""

    VERSION = 1

    def __init__(self):
        """Initialize the flow."""
        self._errors = {}
        self._data = {}

    async def async_step_user(self, user_input=None):
        """Handle the initial step of the configuration."""
        if user_input is not None:
            # Validierung und Speichern der Konfiguration
            self._data = user_input
            return self.async_create_entry(
                title="V-ZUG Integration",
                data=self._data,
            )

        # Zeige das Konfigurationsformular an
        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=self._errors,
        )
