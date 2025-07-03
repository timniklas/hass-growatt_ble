
import asyncio
import struct
from bleak import BleakClient, BleakScanner, BleakError
from .const import REGISTERS

def crc16_modbus(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc

def xor_growatt(payload: bytes) -> bytes:
    key = b"Growatt"
    out = bytearray(payload)
    for i in range(8, len(payload)):
        out[i] = out[i] ^ key[(i-8) % len(key)]
    return bytes(out)

def split_chunks(data: bytes, chunk_size=20):
    return [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

def build_modbus_read(addr, reg_addr, reg_len):
    frame = struct.pack(">B B H H", addr, 3, reg_addr, reg_len)
    crc = crc16_modbus(frame)
    frame += struct.pack("<H", crc)
    return frame

def build_protocol_frame(payload: bytes) -> bytes:
    len_inner = len(payload)
    len_outer = len(payload) + 8
    out = struct.pack(">II", len_inner, len_outer) + payload
    out = xor_growatt(out)
    return out

def parse_response(data: bytes) -> bytes:
    key = b"Growatt"
    out = bytearray(data)
    for i in range(8, len(data)):
        out[i] = out[i] ^ key[(i-8) % len(key)]
    return bytes(out[8:])

def getNegativNum(i):
    return i - 65536 if i > 32767 else i

class GrowattBLE:
    def __init__(self, target_name, char_uuid="0000ff01-0000-1000-8000-00805f9b34fb", device_address=1):
        self.target_name = target_name
        self.char_uuid = char_uuid
        self.device_address = device_address
        self.address = None
        self.client = None
        self._connected = False

    async def find_device(self):
        devices = await BleakScanner.discover(timeout=10.0)
        for d in devices:
            if d.name == self.target_name:
                self.address = d.address
                return True
        return False

    async def ensure_connected(self):
        # Nur suchen, wenn wir die Adresse noch nicht kennen
        if self.address is None:
            await self.find_device()
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
    
    async def send_request(self, client, data: bytes):
        chunks = split_chunks(data)
        for chunk in chunks:
            await client.write_gatt_char(self.char_uuid, chunk)
            await asyncio.sleep(0.05)
        resp = await client.read_gatt_char(self.char_uuid)
        return parse_response(resp)

    async def _read_register(self, client, reg_addr, length=1):
        req_frame = build_modbus_read(self.device_address, reg_addr, length)
        prot_frame = build_protocol_frame(req_frame)
        resp = await self.send_request(client, prot_frame)
        return resp

    async def disconnect(self):
        if self.client is not None and self._connected:
            try:
                await self.client.disconnect()
            except Exception:
                pass
            self._connected = False

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
                    data = await self._read_register(self.client, reg, length)
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
