import logging
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .growatt_ble import GrowattBLE

_LOGGER = logging.getLogger(__name__)
# Intervall auf 1 Sekunde setzen
SCAN_INTERVAL = timedelta(seconds=1)

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
            # Fehlerbehandlung für "nachts nicht erreichbar"
            if "Kein passendes Gerät" in str(exc) or "Device not found" in str(exc) or "not found" in str(exc):
                # Gerät ist nachts aus, das ist normal – gib leere Daten zurück
                _LOGGER.debug("Growatt BLE Gerät nicht erreichbar – vermutlich Nacht. Setze alle Sensoren auf None.")
                return {}
            raise UpdateFailed(f"Growatt BLE update failed: {exc}")
