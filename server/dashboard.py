#!/bin/env python3

from flask import Flask
from dashboard_index import bp_index

app = Flask(__name__, static_folder="assets", static_url_path="/assets")

# Register the blueprints (each with its own routes)
app.register_blueprint(bp_index)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)

