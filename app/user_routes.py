from flask import Blueprint, request, jsonify, make_response, abort
from app import db
import os
import requests
from app.models.user import User
from app.models.event import Event

users_bp = Blueprint('users', __name__, url_prefix="/users")

def validate_complete_request(request_body):
    try:
        if not "" in request_body:
            return request_body

    except:
        abort(make_response({"details": "Invalid data"}, 400))


def validate_model_id(cls, model_id):
    try:
        model_id = int(model_id)    
    except:
        abort(make_response({"details": "Invalid data"}, 404))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details": "Invalid data"}, 404))
    
    return model


@users_bp.route("", methods=["POST"])
def create_user():
    request_body = request.get_json()
    valid_data = validate_complete_request(request_body)
    new_user = User.from_dict(valid_data)

    db.session.add(new_user)
    db.session.commit()

    user_response = {
        "user": new_user.to_dict()
    }
    return make_response(jsonify(user_response), 201)


@users_bp.route("", methods=["GET"])
def read_all_users():
    users = User.query.all()
    users_response = [user.to_dict() for user in users]

    return make_response(jsonify(users_response), 200)


@users_bp.route("/<user_id>", methods=["GET"])
def read_one_user(user_id):
    user = validate_model_id(User, user_id)
    user_response = {
        "user": user.to_dict()
    }
    return make_response(jsonify(user_response), 200)

@users_bp.route("/<user_id>", methods=["PUT"])
def update_user_entire_entry(user_id):
    user = validate_model_id(User, user_id)
    request_body = request.get_json()
    user.first_name=request_body["first_name"]
    user.last_name=request_body["last_name"]
    user.cohort=request_body["cohort"]
    user.location=request_body["location"]
    user.email=request_body["email"]
    user.email=request_body["password"]

    db.session.commit()

    user_response = {
        "user": user.to_dict()
    }
    return make_response((user_response), 200)

@users_bp.route("/<user_id>", methods=["PATCH"])
def update_user_partial_entry(user_id):
    user = validate_model_id(User, user_id)
    request_body = request.get_json()
    user.first_name=request_body["first_name"],
    user.last_name=request_body["last_name"],
    user.cohort=request_body["cohort"],
    user.location=request_body["location"],
    user.email=request_body["email"]
    user.email=request_body["password"]

    db.session.commit()

    user_response = {
        "user": user.to_dict()
    }
    return make_response((user_response), 200)


@users_bp.route("/<user_id>", methods=["DELETE"])
def user_delete(user_id):
    user = validate_model_id(User, user_id)

    db.session.delete(user)
    db.session.commit()

    return make_response({'details': f'User {user.id} successfully deleted'}, 200)