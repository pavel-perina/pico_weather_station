from flask import Blueprint, render_template, jsonify
import json
from datetime import datetime

bp_index =Blueprint("index",__name__)

JSON_FILE = "last_sta01.txt"

@bp_index.route("/")
def index_page():
    # Load the last JSON entry
    try:
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
            dt = datetime.strptime(data["time"], "%Y-%m-%dT%H:%M:%SZ")
            data["time"] = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except (IOError, ValueError):
        return jsonify({"error": "File not found"}), 500

    # A simple HTML template to show data    

    return render_template("index.html", **data)

