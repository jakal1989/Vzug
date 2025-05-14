from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol
import aiohttp
import logging

DOMAIN = "vzug"
_LOGGER = logging.getLogger(__name__)

class VzugConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self.device_type = None
        self.ip_address = None

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Erster Schritt: Gerät auswählen."""
        if user_input is not None:
            self.device_type = user_input["device_type"]
            return await self.async_step_ip()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("device_type"): vol.In(["Ofen", "Geschirrspüler"]),
            }),
        )

    async def async_step_ip(self, user_input=None) -> FlowResult:
        """Zweiter Schritt: IP-Adresse eingeben und Verbindung prüfen."""
        errors = {}

        if user_input is not None:
            self.ip_address = user_input["ip_address"]
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"http://{self.ip_address}/rest", timeout=5) as response:
                        if response.status != 200:
                            raise Exception("Kein 200 OK")
                        data = await response.json()
            except Exception as e:
                _LOGGER.error("Verbindung zum Gerät fehlgeschlagen: %s", e)
                errors["base"] = "cannot_connect"
                return self.async_show_form(
                    step_id="ip",
                    data_schema=vol.Schema({
                        vol.Required("ip_address", default=self.ip_address): str,
                    }),
                    errors=errors,
                )

            # Erfolg: Konfiguration speichern
            return self.async_create_entry(
                title=f"{self.device_type} ({self.ip_address})",
                data={
                    "device_type": self.device_type,
                    "ip_address": self.ip_address,
                    # optional: 'initial_data': data
                },
            )

        return self.async_show_form(
            step_id="ip",
            data_schema=vol.Schema({
                vol.Required("ip_address"): str,
            }),
            errors=errors,
        )
            data_schema=DATA_SCHEMA,
            errors=self._errors,
        )
