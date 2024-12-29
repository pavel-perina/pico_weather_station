#!/usr/bin/env python3

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Configuration
LOG_FILE = "data_log.txt"

# Endpoint to receive and process data
@app.route('/upload', methods=['POST'])
def upload_data():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Invalid or missing JSON"}), 400
        
        # Append the data to the log file
        with open(LOG_FILE, "a") as file:
            file.write(json.dumps(data) + "\n")
        
        print(f"Received and logged data: {data}")
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error processing data: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

# Run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

