#!/usr/bin/python3
""" returns json status of a program """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status_view():
    """returns status of the program"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """returns the count of all class objects"""
    res_dict = {
        'states': storage.count('State'),
        'cities': storage.count('City'),
        'users': storage.count('User'),
        'amenities': storage.count('Amenity'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review')
    }
    return jsonify(res_dict)
