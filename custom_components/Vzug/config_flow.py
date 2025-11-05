import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Optional('device_ips', default=''): str,
    vol.Optional('name_prefix', default='V-ZUG'): str,
})

class VzugConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(step_id='user', data_schema=STEP_USER_DATA_SCHEMA)

        raw = user_input.get('device_ips', '') or ''
        raw = raw.strip()
        ips = []
        if raw:
            for part in raw.replace(',', '\n').split('\n'):
                p = part.strip()
                if p:
                    ips.append(p)

        devices = []
        for idx, ip in enumerate(ips, start=1):
            devices.append({
                'ip': ip,
                'name': f"{user_input.get('name_prefix', 'V-ZUG')} {idx}"
            })

        data = {
            'devices': devices
        }
        return self.async_create_entry(title="V-ZUG (local)", data=data)

    async def async_step_import(self, import_data):
        return await self.async_step_user(import_data)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)

class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is None:
            schema = vol.Schema({
                vol.Optional('add_device_ip', default=''): str,
                vol.Optional('scan_interval', default=120): int,
            })
            return self.async_show_form(step_id='init', data_schema=schema)

        new_ip = user_input.get('add_device_ip', '') or ''
        devices = list(self.config_entry.data.get('devices', []))
        if new_ip.strip():
            devices.append({'ip': new_ip.strip(), 'name': f"V-ZUG {len(devices)+1}"})

        return self.async_create_entry(title="options", data={'scan_interval': user_input.get('scan_interval', 120), 'devices': devices})
