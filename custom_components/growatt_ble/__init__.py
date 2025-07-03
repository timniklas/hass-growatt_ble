from .const import DOMAIN
from .sensor import GrowattBLECoordinator

async def async_setup_entry(hass, entry):
    coordinator = GrowattBLECoordinator(hass, entry.data["serial"])
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass, entry):
    coordinator = hass.data[DOMAIN].pop(entry.entry_id, None)
    if coordinator is not None:
        await coordinator.ble.disconnect()
    await hass.config_entries.async_forward_entry_unloads(entry, ["sensor"])
    return True
