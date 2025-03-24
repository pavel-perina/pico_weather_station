Here are files related to weather station server running on Linux. Requirements are Python with some libraries, optionally PostgreSQL. Many variables are hardcoded.

## Server Files

These files are part of Python/Flask server which handles both uploads from Raspberry Pi Pico and displaying of recent data (dashboard).

| File | Description |
|:-----|:------------|
| `server.py` | Flask web server, main program |
| `server_index.py` | Main page, serves `/` displays data |
| `server_upload_to_jsonl.py` | `/upload` handles uploads of JSON from Raspberry Pico to JSONL file |
| `server_upload_to_psql.py` | `/upload` handles uploads of JSON from Raspberry Pico to PostgreSQL database |
| `weather_calculations.py` | Calculations of sea level pressure, specific humidity and dew point |
| `assets/` | CSS styles, images, ... |
| `templates/` | HTML templates |

## Script Files (Automation)

These are used for regenerating static content or database backups.

| File | Description |
|:-----|:------------|
| `update_last_month_pressure.sh` | Update monthly pressure graph|
| `update_last_month_temperature.sh` | Update monthly temperature graph |
| `update_recent.sh` | Update recent graphs |

## Other files
| File | Description |
|:-----|:------------|
| `.gitignore` | Files ignored by git versioning system |
| `README.md` | This file |
| `log_sta01.jsonl.zst` | Compressed sample data from first half of January 2025 |


## Version history

* 2024-12-28: Very first version just to test functionality.
* 2024-01-02: Calculated fields, dashboard
* 2024-01-15: Plotting scripts
* 2024-01-17: Merged servers for upload and dashboard (index)
* 2024-01-20: Added options to add data into database instead of JSONL file
* 2024-01-20: `git update-index --assume-unchanged assets/img/weather_sta01_recent_*`
