#!/usr/bin/python3
""" returns json status of a program """
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status_view():
    """returns status of the program"""
    if request.method == 'GET':
        return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def stats():
    """returns the count of all class objects"""
    if request.method == 'GET':
        res = {}
        OBJ = {
            "Amenity": "amenities",
            "City": "cities",
            "Places": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }

        for key, value in OBJ.items():
            res[value] = storage.count(key)
        return jsonify(res)
