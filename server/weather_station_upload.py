#!/usr/bin/env python3

from flask import Flask, request, jsonify
import json
from datetime import datetime, timezone
from weather_calculations import get_derived_data

app = Flask(__name__)


# Configuration
LOG_FILE = "data_log.txt"

class Station():
    def __init__(self, id:str, altitude:float, outdoor:bool):
        self.id       = id
        self.altitude = altitude
        self.outdoor  = outdoor

stations = [ Station("sta01", 250.0, False)]
station_dict = {station.id: station for station in stations}
       
# Endpoint to receive and process data
@app.route('/upload', methods=['POST'])
def upload_data():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Invalid or missing JSON"}), 400

        # Add time of arrival
        toa = datetime.now(timezone.utc)
        data["time_of_arrival"] = f"{toa.year}-{toa.month:02d}-{toa.day:02d}T{toa.hour:02d}:{toa:minute:02d}:{toa:second:02d}Z"

        # Add additional data for known stations
        station = station_dict.get(data["station_id"])
        if (station):
            additional_data = get_derived_data(data["temperature"], data["humidity"], data["pressure"], station.altitude, station.outdoor)
            for key, value in additional_data:
                data[key] = value

            # Append the data to the log file
            with open(f"log_{data["station_id"]}.txt", "a") as file:
                file.write(json.dumps(data) + "\n")
                
            print(f"Received and logged data: {data}")
            return jsonify({"status": "success"}), 200
        else:
            print("Unknown station")
            return jsonify({"status": "error", "message": "Internal server error"}), 500
        
    except Exception as e:
        print(f"Error processing data: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

# Run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

