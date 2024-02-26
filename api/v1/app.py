#!/usr/bin/python3
""" app.py file """
import os
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
db = os.environ.get('HBNB_TYPE_STORAGE', 'json_file')
host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
port = os.environ.get('HBNB_API_PORT', '5000')

# Set URL map to allow for non-strict slashes
app.url_map.strict_slashes = False

# Register blueprint for API views
app.register_blueprint(app_views)

# Enable CORS for all API routes
CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})

# Teardown function to close storage connection after each request
@app.teardown_appcontext
def close_storage(exception):
    """close storage"""
    storage.close()

# Error handler for 404 Not Found errors
@app.errorhandler(404)
def not_found_error(error):
    """error 404"""
    return jsonify({"error": "Not found"}), 404

# Run the Flask app
if __name__ == '__main__':
    app.run(host=host, port=int(port), threaded=True)
