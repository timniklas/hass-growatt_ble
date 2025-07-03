import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .growatt_ble import GrowattBLE

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=60)

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
