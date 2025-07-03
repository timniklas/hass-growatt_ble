import logging
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN, REGISTERS
from .coordinator import GrowattBLECoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    serial = entry.data["serial"]
    coordinator = GrowattBLECoordinator(hass, serial)
    await coordinator.async_config_entry_first_refresh()
    sensors = [
        GrowattBLESensor(coordinator, key, meta)
        for key, meta in REGISTERS.items()
    ]
    async_add_entities(sensors, True)

class GrowattBLESensor(SensorEntity):
    def __init__(self, coordinator, key, meta):
        self.coordinator = coordinator
        self.key = key
        self.meta = meta
        self._attr_name = f"Growatt BLE {key.replace('_',' ').title()}"
        self._attr_unique_id = f"growatt_ble_{coordinator.ble.target_name}_{key}"
        self._attr_native_unit_of_measurement = meta.get("unit", "")
        self._attr_state_class = "measurement"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.coordinator.ble.target_name)},
            "name": f"Growatt BLE ({self.coordinator.ble.target_name})",
            "manufacturer": "Growatt",
            "model": "NEO 800",
            "serial_number": self.coordinator.ble.target_name,
        }

    @property
    def available(self):
        return self.coordinator.data is not None and self.key in self.coordinator.data

    @property
    def native_value(self):
        if self.coordinator.data:
            return self.coordinator.data.get(self.key)
        return None

    async def async_update(self):
        await self.coordinator.async_request_refresh()
