import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    coordinator = hass.data[DOMAIN][entry.entry_id]['coordinator']
    devices = entry.data.get('devices', [])
    entities = []
    for dev in devices:
        ip = dev.get('ip')
        name = dev.get('name', ip)
        entities.append(VzugDeviceSensor(coordinator, entry, ip, name))
    async_add_entities(entities, update_before_add=True)

class VzugDeviceSensor(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, ip, name):
        self.coordinator = coordinator
        self._entry = entry
        self._ip = ip
        self._name = name
        self._attr_name = name
        self._attr_unique_id = f"vzug_{ip}"

    @property
    def native_value(self):
        data = self.coordinator.data.get(self._ip, {})
        if isinstance(data, dict):
            if 'Program' in data:
                return data.get('Program')
            if 'Status' in data:
                return data.get('Status')
        return str(data)

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data.get(self._ip, {})
        if isinstance(data, dict):
            return data
        return {'error': data}
