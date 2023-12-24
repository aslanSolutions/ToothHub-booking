from venv import logger
from flask import Blueprint, jsonify, request
from apifairy import body, response
from .schema import WishlistSchema
from.db import users
from bson import ObjectId 
import requests
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('Wishlist', __name__, url_prefix='/wishlist')
wishlist_collection = users
Wishlists_Schema = WishlistSchema(many=True)

@bp.route('/create', methods=['POST'])
@jwt_required()
def register_wishlist():
    # Create wishlist
    payload = request.get_json()
    logger.debug(f"Received payload: {payload}")

    auth_header = request.headers.get('Authorization')
    logger.debug(f"Authorization header received: {auth_header}")
    # Instantiate the schema and validate the payload
    schema = WishlistSchema()
    errors = schema.validate(payload)
    if errors:
        return jsonify({"message": "Validation error", "errors": errors}), 400

    # Extract the JWT identity from the request
    current_user_identity = get_jwt_identity()

    # Make a validation request to the authentication service
    validate_url = "http://127.0.0.1:5005/auth/validate"
    headers = {"Authorization": request.headers.get('Authorization')}
    validate_response = requests.get(validate_url, headers=headers)

    if validate_response.status_code == 200:
        # User is valid, proceed with wishlist creation
        result = wishlist_collection.insert_one(payload)
        new_wishlist_id = result.inserted_id
        created_wishlist = wishlist_collection.find_one({'_id': new_wishlist_id})

        # Convert ObjectId to string before returning the response
        created_wishlist['_id'] = str(created_wishlist['_id'])
        return jsonify(created_wishlist), 201
    else:
        # Validation failed
        return jsonify({"message": "User validation failed"}), validate_response.status_code



@bp.route('/<int:wishlist_id>', methods=['GET'])
@response(WishlistSchema, 200)
def get_wishlist(wishlist_id):
    wishlist = users.find_one({'_id': wishlist_id})
    if wishlist:
        return wishlist
    else:
        return jsonify({"message": f"No wishlist found with ID {wishlist_id}"}), 404


@bp.route('/<int:patient_id>', methods=['GET'])
@response(WishlistSchema, 200)
def get_all_wishlists_for_patient(patient_id):
    all_wishlist_for_patient = list(wishlist_collection.find({'patient_id': patient_id}))
    return all_wishlist_for_patient



@bp.route('/<int:wishlist_id>', methods=['DELETE'])
def delete_wishlist(wishlist_id):
    result = users.delete_one({'_id': wishlist_id})

    if result.deleted_count == 1:
        return jsonify({"message": f"wishlist with ID {wishlist_id} deleted successfully"}), 200
    else:
        return jsonify({"message": f"No dentist found with ID {wishlist_id}"}), 404


def get_wishlists(date):
    wishlist = users.find({"date":date})
    wishlists = list(wishlist)

    # Convert ObjectId to string for JSON serialization
    for wishlist in wishlists:
        wishlist['_id'] = str(wishlist['_id'])

    if wishlist:
        return jsonify(wishlists)
    else:
        return jsonify({"message": f"No wishlist matches the spesific date: {date}"}), 404