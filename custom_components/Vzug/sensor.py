from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up V-ZUG sensors from config entry."""
    device_type = entry.data["device_type"]
    ip_address = entry.data["ip_address"]

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://{ip_address}/ai?command=getDeviceStatus") as response:
                data = await response.json()
    except Exception as e:
        _LOGGER.error("Fehler beim Abrufen der Gerätedaten: %s", e)
        return

    entities = []
    for key, value in data.items():
        entities.append(VZugSensor(key, value, device_type, ip_address))

    async_add_entities(entities, True)

class VZugSensor(SensorEntity):
    """Ein Sensor pro JSON-Key."""

    def __init__(self, key, value, device_type, ip):
        self._attr_name = f"{device_type} - {key}"
        self._attr_unique_id = f"{device_type.lower()}_{ip}_{key.lower()}"
        self._state = value
        self._key = key
        self._ip = ip
        self._device_type = device_type
        self._attr_icon = "mdi:checkbox-marked-circle-outline"  # oder besser je nach key

    @property
    def state(self):
        return self._state

    async def async_update(self):
        """Hole aktuelle Daten vom Gerät."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://{self._ip}/ai?command=getDeviceStatus") as response:
                    data = await response.json()
                    self._state = data.get(self._key)
        except Exception as e:
            _LOGGER.error("Update fehlgeschlagen für %s: %s", self._attr_name, e)
            self._state = None
