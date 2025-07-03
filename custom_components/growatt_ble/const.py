DOMAIN = "growatt_ble"

REGISTERS = {
    "output_power": {"reg": 2,  "scale": 0.25,  "unit": "W"},
    "pv1_voltage":  {"reg": 5,  "scale": 0.1,  "unit": "V"},
    "pv1_current":  {"reg": 6,  "scale": 0.005, "unit": "A"},
    "pv2_voltage":  {"reg": 7,  "scale": 0.1,  "unit": "V"},
    "pv2_current":  {"reg": 8,  "scale": 0.005,  "unit": "A"},
    "pv1_power":    {"reg": 9,  "scale": 0.1,    "unit": "W"},
    "pv2_power":    {"reg": 10, "scale": 0.1,    "unit": "W"},
    "daily_energy": {"reg": 11, "scale": 0.005,  "unit": "kWh"},
    "total_energy": {"reg": 13, "scale": 0.1,  "unit": "kWh"},
    "device_temp":  {"reg": 14, "scale": 0.1,  "unit": "°C"},
    "boost_temp":   {"reg": 15, "scale": 0.1,  "unit": "°C"},
}
