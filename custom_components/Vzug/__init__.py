"""The V-ZUG Integration."""

from homeassistant import config_entries, core
from homeassistant.const import CONF_IP_ADDRESS

DOMAIN = "vzug"

async def async_setup(hass: core.HomeAssistant, config: dict):
    """Set up the V-ZUG integration."""
    return True

async def async_setup_entry(hass: core.HomeAssistant, entry: config_entries.ConfigEntry):
    """Set up V-ZUG from a config entry."""
    # Hier kannst du weitere Initialisierungen vornehmen
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    return True

async def async_unload_entry(hass: core.HomeAssistant, entry: config_entries.ConfigEntry):
    """Unload a config entry."""
    if DOMAIN in hass.data:
        hass.data[DOMAIN].pop(entry.entry_id)
    return True
