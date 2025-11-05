"""V-ZUG custom integration (LAN-only, multiple devices per config entry)."""
from __future__ import annotations
import asyncio
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, PLATFORMS, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    # Each config entry stores a list of devices under 'devices' key
    devices = entry.data.get('devices', [])
    coordinator = VzugCoordinator(hass, entry, devices)
    await coordinator.async_config_entries_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = {
        'coordinator': coordinator,
        'devices': devices,
        'entry': entry,
    }

    # forward setup to platforms
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = all(
        await asyncio.gather(
            *[hass.config_entries.async_forward_entry_unload(entry, platform) for platform in PLATFORMS]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

class VzugCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch data for all configured V-ZUG devices."""
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, devices: list):
        super().__init__(
            hass,
            _LOGGER,
            name=f"vzug_coordinator_{entry.entry_id}",
            update_interval=entry.options.get('scan_interval', DEFAULT_SCAN_INTERVAL)
        )
        self._entry = entry
        self.devices = devices  # list of dicts: {'ip': '192.168.x.x', 'name': 'oven'}
        self.data = {}

    async def _async_update_data(self) -> dict:
        """Fetch data from each device."""
        results = {}
        session = hass.helpers.aiohttp_client.async_get_clientsession()
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
                # store raw result (value_json.result expected)
                results[ip] = json_data.get('result', json_data)
            except Exception as err:
                _LOGGER.debug("Error fetching V-ZUG device %s: %s", ip, err)
                results[ip] = {'error': str(err)}
        self.data = results
        return results
