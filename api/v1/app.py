#!/usr/bin/python3
"""Script for starting Flask web application
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from os import getenv
from flask_cors import CORS


app = Flask(__name__)

CORS(app, resources = {r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Removes current SQLAlchemy session"""
    storage.close()


@app.errorhandler(404)
def notFound(error):
    """Returns status of the 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
