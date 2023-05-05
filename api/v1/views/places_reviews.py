#!/usr/bin/python3
"""Create new view for Place Reviews objects"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.review import Review


@app_views('/places/<place_id>/reviews', methods=['GET', 'POST'])
def reviews(place_id):
    """retrieves list of all Review objects of place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify([rev.to_dict() for rev in place.reviews])

    res = request.get_json(silent=True)
    if res is None:
        abort(400, "Not a JSON")
    user_id = res.get("user_id")
    if user_id is None:
        abort(400, "Missing user_id")
    if storage.get("User", user_id) is None:
        abort(404)
    if res.get("text") is None:
        abort(400, "Missing text")
    res["place_id"] = place_id
    review = Review(**res)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def review_id(review_id):
    """Updates a review object"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    elif request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    res = request.get_json(silent=True)
    if res is None:
        abort(400, "Not a JSON")
    avoid = {"id", "user_id", "place_id", "created_at", "updated_at"}
    [setattr(review, k, v) for k, v in res.items(), if k not in avoid]
    review.save()
    return jsonify(review.to_dict()), 200
