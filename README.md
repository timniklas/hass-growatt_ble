# Growatt BLE Home Assistant Integration

![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)
![license](https://img.shields.io/github/license/timniklas/growatt_ble)
![maintenance](https://img.shields.io/maintenance/yes/2025)

Integriere deine Growatt NEO 800 (und ähnliche) Geräte per Bluetooth Low Energy direkt in Home Assistant und erhalte PV-Daten wie Leistung, Spannung, Energie, Temperatur u.v.m. Die Geräte-Seriennummer wird beim Hinzufügen der Integration abgefragt.

## Features

- Automatische Erkennung des Growatt BLE Geräts per Seriennummer (Gerätename)
- Sensoren für:
  - PV1 / PV2 Spannung, Strom & Leistung
  - Output Power
  - Tages- & Gesamtenergie
  - Temperatur(en)
- Konfigurierbar via Home Assistant UI (Config Flow)
- Fehlerprüfung: Gerät muss bei Einrichtung erreichbar sein
- Mehrere Geräte werden unterstützt

## Installation

**HACS:**  
Dieses Repository als [benutzerdefiniertes Repository](https://hacs.xyz/docs/faq/custom_repositories/) in HACS hinzufügen und "Growatt BLE" installieren.

**Manuell:**  
1. Lade das Repo herunter und kopiere den Ordner `growatt_ble` in das Verzeichnis `custom_components` deiner Home Assistant Installation.
2. Starte Home Assistant neu.

> **Voraussetzungen:**  
> - Bluetooth-Adapter auf dem Home Assistant Host  
> - Das Growatt-Gerät muss eingeschaltet und in Bluetooth-Reichweite sein  
> - Das Python-Paket `bleak` wird automatisch installiert

## Einrichtung

1. Füge über die Home Assistant Oberfläche die Integration "Growatt BLE" hinzu.
2. Gib die Seriennummer (Gerätename) deines Geräts ein.
3. Nach erfolgreicher Erkennung werden die Sensoren automatisch erstellt.

## Geräte-Namen (Seriennummer) finden

Im Normalfall steht der Gerätename auf dem Typenschild des Growatt Geräts und sieht aus wie `QMNxxxxxxx`.

## Bekannte Probleme

- Das Gerät muss für die Ersteinrichtung eingeschaltet und in Bluetooth-Reichweite sein.
- Nur getestet mit NEO 800, andere Modelle könnten abweichende Register haben.
- Die BLE-Kommunikation ist empfindlich gegenüber Zeitüberschreitungen.

## Beispiel-Sensoren

- `sensor.growatt_ble_output_power`
- `sensor.growatt_ble_pv1_voltage`
- `sensor.growatt_ble_daily_energy`
- u.v.m.

## Roadmap & Ideen

- Unterstützung für weitere Growatt-Modelle/Register
- Optionale Konfiguration von Scan-Intervallen
- Automatische Erkennung mehrerer Geräte

## Support & Feedback

Fragen, Feature-Wünsche oder Fehler?  
Erstelle ein [Issue](https://github.com/timniklas/growatt_ble/issues) oder diskutiere auf GitHub!

## Lizenz

[MIT License](LICENSE)
