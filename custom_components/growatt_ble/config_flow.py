from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN
from .growatt_ble import GrowattBLE

class GrowattBLEConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            serial = user_input["serial"]
            if not serial or len(serial) < 8:
                errors["serial"] = "invalid_serial"
            else:
                ble = GrowattBLE(target_name=serial)
                found = await ble.find_device()
                if not found:
                    errors["serial"] = "not_found"
                else:
                    return self.async_create_entry(
                        title=f"Growatt BLE ({serial})",
                        data={"serial": serial}
                    )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("serial"): str,
            }),
            errors=errors,
        )
