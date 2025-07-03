import logging
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, REGISTERS
from .growatt_ble import GrowattBLE

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=60)

async def async_setup_entry(hass, entry, async_add_entities):
    serial = entry.data["serial"]
    coordinator = GrowattBLECoordinator(hass, serial)
    await coordinator.async_config_entry_first_refresh()
    sensors = [
        GrowattBLESensor(coordinator, key, meta)
        for key, meta in REGISTERS.items()
    ]
    async_add_entities(sensors, True)

class GrowattBLECoordinator(DataUpdateCoordinator):
    def __init__(self, hass, serial):
        super().__init__(
            hass,
            _LOGGER,
            name=f"Growatt BLE Coordinator ({serial})",
            update_interval=SCAN_INTERVAL,
        )
        self.ble = GrowattBLE(target_name=serial)

    async def _async_update_data(self):
        try:
            data = await self.ble.read_all()
            return data
        except Exception as exc:
            raise UpdateFailed(f"Growatt BLE update failed: {exc}")

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
