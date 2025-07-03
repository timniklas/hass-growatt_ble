import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .growatt_ble import GrowattBLE

_LOGGER = logging.getLogger(__name__)
# Intervall für normalen Betrieb
SCAN_INTERVAL = timedelta(seconds=1)
# Intervall wenn das Gerät nicht erreichbar ist (z.B. nachts)
SCAN_INTERVAL_UNREACHABLE = timedelta(seconds=60)

class GrowattBLECoordinator(DataUpdateCoordinator):
    def __init__(self, hass, serial):
        super().__init__(
            hass,
            _LOGGER,
            name=f"Growatt BLE Coordinator ({serial})",
            update_interval=SCAN_INTERVAL,
        )
        self.ble = GrowattBLE(target_name=serial)
        self._last_update_success = True

    async def _async_update_data(self):
        try:
            data = await self.ble.read_all()
            # Gerät war erreichbar -> zurück auf kurzes Intervall
            if not self._last_update_success:
                self.update_interval = SCAN_INTERVAL
                await self.async_request_refresh()
            self._last_update_success = True
            return data
        except Exception as exc:
            # Fehlerbehandlung für "nachts nicht erreichbar"
            if "Kein passendes Gerät" in str(exc) or "Device not found" in str(exc) or "not found" in str(exc):
                _LOGGER.debug("Growatt BLE Gerät nicht erreichbar – vermutlich Nacht. Setze alle Sensoren auf None.")
                # Setze langes Intervall
                if self._last_update_success:
                    self.update_interval = SCAN_INTERVAL_UNREACHABLE
                    await self.async_request_refresh()
                self._last_update_success = False
                return {}
            raise UpdateFailed(f"Growatt BLE update failed: {exc}")
