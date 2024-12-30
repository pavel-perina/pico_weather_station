```
   ____                 _                          ____  _
  |  _ \ __ _ ___ _ __ | |__   ___ _ __ _ __ _   _|  _ \(_) ___ ___
  | |_) / _` / __| '_ \| '_ \ / _ \ '__| '__| | | | |_) | |/ __/ _ \
  |  _ < (_| \__ \ |_) | |_) |  __/ |  | |  | |_| |  __/| | (_| (_) |
  |_| \_\__,_|___/ .__/|_.__/ \___|_|  |_|   \__, |_|   |_|\___\___/
                 |_|                         |___/
__        __         _   _               ____  _        _   _
\ \      / /__  __ _| |_| |__   ___ _ __/ ___|| |_ __ _| |_(_) ___  _ __
 \ \ /\ / / _ \/ _` | __| '_ \ / _ \ '__\___ \| __/ _` | __| |/ _ \| '_ \
  \ V  V /  __/ (_| | |_| | | |  __/ |   ___) | || (_| | |_| | (_) | | | |
   \_/\_/ \___|\__,_|\__|_| |_|\___|_|  |____/ \__\__,_|\__|_|\___/|_| |_|

```

Raspberry Pico W Weather Station project(s)

## server/

Contains server. As of 2024-12-30 it basically appends any received json
data to a file. 

## snippets/

This directory contains prototyping code snippets for a weather station,
such as interfacing PCD8544 SPI display, experiments with WiFi and BLE
connectivity and sensor readings. Some auxiliary scripts are also present
here.
