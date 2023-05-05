#!/usr/bin/python3
"""returns json status of a program"""
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route("/status", strict_slashes=False)
def status_view():
    """returns status of the program"""
    return jsonify({"status": "OK"})
