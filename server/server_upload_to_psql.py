#!/usr/bin/env python3

from flask import Blueprint, request, jsonify
import json
from datetime import datetime, timezone
from weather_calculations import get_derived_data
import logging
import sys
# pip install psycopg2-binary sqlalchemy
import sqlalchemy

#########################################################################################################
#   ____             __ _                       _   _
#  / ___|___  _ __  / _(_) __ _ _   _ _ __ __ _| |_(_) ___  _ __
# | |   / _ \| '_ \| |_| |/ _` | | | | '__/ _` | __| |/ _ \| '_ \
# | |__| (_) | | | |  _| | (_| | |_| | | | (_| | |_| | (_) | | | |
#  \____\___/|_| |_|_| |_|\__, |\__,_|_|  \__,_|\__|_|\___/|_| |_|
#                         |___/

LOG_FILE = "server_log.txt"

class Station():
    def __init__(self, id:str, altitude:float, outdoor:bool):
        self.id       = id
        self.altitude = altitude
        self.outdoor  = outdoor

stations = [ Station("sta01", 250.0, False)]
station_dict = {station.id: station for station in stations}

SQL_CON_STR = "postgresql:///weather_data?host=/home/pavel/postgre-sockets"
SQL_INSERT = """
    INSERT INTO weather_data (
        station_id,
        timestamp,
        temperature,
        pressure_at_station,
        humidity,
        dew_point,
        pressure_at_sea_level,
        specific_humidity
    ) VALUES (
        :station_id,
        :time,
        :temperature,
        :pressure,
        :humidity,
        :dew_point,
        :sea_level_pressure,
        :specific_humidity
    )"""

#########################################################################################################
#  _                      _
# | |    ___   __ _  __ _(_)_ __   __ _
# | |   / _ \ / _` |/ _` | | '_ \ / _` |
# | |__| (_) | (_| | (_| | | | | | (_| |
# |_____\___/ \__, |\__, |_|_| |_|\__, |
#             |___/ |___/         |___/

def createLogger() -> logging.Logger:
    """Create and initialize logger for this script"""
    # Create a formatter with desired format (including timestamp and level)
    formatter = logging.Formatter('%(asctime)-24s%(levelname)-8s: %(message)s')

    # Create a file handler
    file_handler = logging.FileHandler(LOG_FILE, encoding="UTF-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)  # Set formatter for file handler

    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)  # Set formatter for console handler

    # Add both handlers to the logger
    logger = logging.getLogger("main")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

logger = createLogger()

#########################################################################################################
#  ____                                              _
# / ___|  ___ _ ____   _____ _ __   _ __   __ _ _ __| |_
# \___ \ / _ \ '__\ \ / / _ \ '__| | '_ \ / _` | '__| __|
#  ___) |  __/ |   \ V /  __/ |    | |_) | (_| | |  | |_
# |____/ \___|_|    \_/ \___|_|    | .__/ \__,_|_|   \__|
#                                  |_|

# Define the blueprint
bp_upload = Blueprint("upload", __name__)

db_engine = sqlalchemy.create_engine(SQL_CON_STR)

# Endpoint to receive and process data
@bp_upload.route('/upload', methods=['POST'])
def upload_data():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        if not data:
            logger.error("Invalid or missing JSON")
            return jsonify({"status": "error", "message": "Invalid or missing JSON"}), 400

        # Add time of arrival
        toa = datetime.now(timezone.utc)
        data["time_of_arrival"] = f"{toa.year}-{toa.month:02d}-{toa.day:02d}T{toa.hour:02d}:{toa.minute:02d}:{toa.second:02d}Z"
        print(data)
        # Add additional data for known stations
        station = station_dict.get(data["station_id"])
        if (station):
            print("known station")
            additional_data = get_derived_data(data["temperature"], data["humidity"], data["pressure"], station.altitude, station.outdoor)
            for key, value in additional_data:
                data[key] = value

            # Append the data to the log file
            #with open(f"log_{data["station_id"]}.jsonl", "a") as file:
            #    file.write(json.dumps(data) + "\n")

            # Insert to database
            with db_engine.connect() as conn:
                conn.execute(sqlalchemy.text(SQL_INSERT), data)
                conn.commit()

            # Last entry for dashboard
            with open(f"last_{data["station_id"]}.json", "w") as file:
                file.write(json.dumps(data) + "\n")

            logger.info(f"Received and logged data: {data}")
            return jsonify({"status": "success"}), 200
        elif "station_id" in data and data["station_id"] != "":
            # Unknown station, fallback to json lines
            print("Unknown station")
            with open(f"last_{data["station_id"]}.json", "w") as file:
                file.write(json.dumps(data) + "\n")
                        # Append the data to the log file
            with open(f"log_{data["station_id"]}.jsonl", "a") as file:
                file.write(json.dumps(data) + "\n")
            return jsonify({"status": "success"}), 200
        else:
            logger.error("Unknown station")
            return jsonify({"status": "error", "message": "Internal server error"}), 500
    except Exception as e:
        
        
        logger.error(f"Error processing data: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500
