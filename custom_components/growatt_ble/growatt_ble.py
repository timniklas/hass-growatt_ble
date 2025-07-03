from bleak import BleakClient, BleakScanner, BleakError

class GrowattBLE:
    def __init__(self, target_name, char_uuid="0000ff01-0000-1000-8000-00805f9b34fb", device_address=1):
        self.target_name = target_name
        self.char_uuid = char_uuid
        self.device_address = device_address
        self.address = None
        self.client = None
        self._connected = False

    async def ensure_connected(self):
        # Nur suchen, wenn wir die Adresse noch nicht kennen
        if self.address is None:
            devices = await BleakScanner.discover(timeout=10.0)
            for d in devices:
                if d.name == self.target_name:
                    self.address = d.address
                    break
        if self.address is None:
            raise Exception(f"Kein passendes Gerät mit Seriennummer '{self.target_name}' gefunden!")

        # Wenn nicht verbunden oder Client nicht vorhanden, neue Verbindung aufbauen
        if self.client is None or not self._connected:
            self.client = BleakClient(self.address)
            try:
                await self.client.connect()
                self._connected = True
            except Exception as exc:
                self._connected = False
                raise Exception(f"Verbindung zu {self.address} fehlgeschlagen: {exc}")

    async def read_all(self):
        try:
            await self.ensure_connected()
            result = {}
            for key, meta in REGISTERS.items():
                reg = meta["reg"]
                scale = meta["scale"]
                unit = meta.get("unit", "")
                length = meta.get("length", 1)
                is_temp = meta.get("temp", False)
                try:
                    data = await self.read_register(self.client, reg, length)
                    if len(data) < 7:
                        continue
                    val = struct.unpack(">H", data[5:7])[0]
                    if is_temp:
                        val = getNegativNum(val)
                    value = val * scale
                    result[key] = value
                except Exception:
                    result[key] = None
            return result
        except (BleakError, Exception) as exc:
            # Verbindung verloren, beim nächsten Mal erneut versuchen
            self._connected = False
            raise exc
