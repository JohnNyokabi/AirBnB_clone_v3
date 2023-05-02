#!/usr/bin/pyhton3
"""Creates new view for places amenities objects"""
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def place_amenities(place_id):
    """Retrieves list of all Amenity objects"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)
    return jsonify([pa.to_dict() for pa in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST', 'DELETE'])
def update_place_amenities(place_id, amenity_id):
    """Updates Amenity object to a place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    exists = False

    if place is None or amenity is None:
        abort(404)

    if request.method == 'POST':
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            if amenity in place.amenities:
                exists = True
            else:
                place.amenities.append(amenity)
        else:
            if amenity.id in place.amenity_ids:
                exists = True
            else:
                place.amenity_ids.append(amenity_id)

        place.save()
        return jsonify(amenity.to_dict()), (200 if exists else 201)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity.id not in place.amenity_ids:
            abort(404)
            place.amenity_ids.remove(amenity.id)
    place.save()
    return jsonify({}), 200
