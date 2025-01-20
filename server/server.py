#!/bin/env python3

from flask import Flask
from server_index import bp_index
#from server_upload_to_jsonl import bp_upload
from server_upload_to_psql import bp_upload

app = Flask(__name__, static_folder="assets", static_url_path="/assets")

# Register the blueprints (each with its own routes)
app.register_blueprint(bp_index)
app.register_blueprint(bp_upload)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
