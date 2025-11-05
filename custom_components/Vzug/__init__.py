"""V-ZUG custom integration (LAN-only, multiple devices per config entry)."""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, PLATFORMS, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    devices = entry.data.get('devices', [])
    coordinator = VzugCoordinator(hass, entry, devices)
    await coordinator.async_config_entries_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = {
        'coordinator': coordinator,
        'devices': devices,
        'entry': entry,
    }
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = all(
        await hass.async_create_task(*[hass.config_entries.async_forward_entry_unload(entry, platform) for platform in PLATFORMS])
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

class VzugCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch data for all configured V-ZUG devices."""
    def __init__(self, hass, entry, devices):
        super().__init__(
            hass,
            _LOGGER,
            name=f"vzug_coordinator_{entry.entry_id}",
            update_interval=timedelta(seconds=entry.options.get('scan_interval', DEFAULT_SCAN_INTERVAL))
        )
        self.hass = hass
        self._entry = entry
        self.devices = devices
        self.data = {}

    async def _async_update_data(self):
        results = {}
        session = self.hass.helpers.aiohttp_client.async_get_clientsession()
        for dev in self.devices:
            ip = dev.get('ip')
            url = f"http://{ip}/ai?command=getDeviceStatus"
            try:
                resp = await session.get(url, timeout=15)
                if resp.status != 200:
                    _LOGGER.debug("V-ZUG device %s returned status %s", ip, resp.status)
                    results[ip] = {'error': f'http_{resp.status}'}
                    continue
                json_data = await resp.json()
                results[ip] = json_data.get('result', json_data)
            except Exception as err:
                _LOGGER.debug("Error fetching V-ZUG device %s: %s", ip, err)
                results[ip] = {'error': str(err)}
        self.data = results
        return results
