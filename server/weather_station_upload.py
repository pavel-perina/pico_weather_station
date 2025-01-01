#!/usr/bin/env python3

from flask import Flask, request, jsonify
import json
from datetime import datetime, timezone
from weather_calculations import get_derived_data
import logging
import sys

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

app = Flask(__name__)
        
# Endpoint to receive and process data
@app.route('/upload', methods=['POST'])
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
            with open(f"log_{data["station_id"]}.txt", "a") as file:
                file.write(json.dumps(data) + "\n")
                
            logger.info(f"Received and logged data: {data}")
            return jsonify({"status": "success"}), 200
        else:
            logger.error("Unknown station")
            return jsonify({"status": "error", "message": "Internal server error"}), 500
        
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

# Run the server
if __name__ == '__main__':
    logger.info("Running server")
    app.run(host='0.0.0.0', port=5000)
    logger.info("Stopping server")

