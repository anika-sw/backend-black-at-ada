from sqlalchemy import func
from flask import Flask, Blueprint, request, jsonify, make_response, abort
from app import db
import os
import requests
from app.models.user import User
from app.models.event import Event
from datetime import datetime
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)


users_bp = Blueprint("users", __name__, url_prefix="/users")


def validate_model_id(cls, model_id):
    try:
        model_id = int(model_id)    
    except:
        abort(make_response({"details": "Invalid data"}, 404))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details": "Invalid data"}, 404))
    
    return model


@users_bp.route("", methods=["GET"])
def read_all_users():
    user_query = User.query.order_by(User.first_name.asc())
    sort_query = request.args.get("sort")
    if sort_query == "lastName":
        user_query = User.query.order_by(User.last_name.asc(), User.first_name.asc())
    if sort_query == "cohort":
        user_query = User.query.order_by(User.cohort.asc())
    if sort_query == "company":
        user_query = User.query.order_by(User.company.asc())
    if sort_query == "salaryAsc":
        user_query = User.query.order_by(User.salary.asc())
    if sort_query == "salaryDesc":
        user_query = User.query.order_by(User.salary.desc())
    if sort_query == "salaryCompany":
        user_query = User.query.order_by(User.company.asc())
    # if sort_query == "nearMe":
    #     user_query = User.db.session.query(User).filter(func.ST_DWithin(User.geoLoc, geo, meters)).order_by(func.ST_Distance(User.geoLoc, geo))

    users = user_query
    users_response = [user.to_dict() for user in users]

    return make_response(jsonify(users_response), 200)


@users_bp.route("/<user_id>", methods=["GET"])
def read_one_user(user_id):
    user = validate_model_id(User, user_id)
    user_response = {
        "user": user.to_dict()
    }
    return make_response(jsonify(user_response), 200)


@users_bp.route("/<user_id>", methods=["PATCH"])
def update_user_entry(user_id):
    user = validate_model_id(User, user_id)
    request_body = request.get_json()

    user.first_name = request_body["first_name"]
    user.last_name = request_body["last_name"]
    user.cohort = request_body["cohort"]
    user.location_name = request_body["location_name"]
    user.location_lat = request_body["location_lat"]
    user.location_lng = request_body["location_lng"]
    user.email = request_body["email"]
    user.profile_pic_url = request_body["profile_pic_url"]
    user.pronouns = request_body["pronouns"]
    user.company = request_body["company"]
    user.linkedin = request_body["linkedin"]
    user.job_title = request_body["job_title"]
    user.salary = request_body["salary"]
    user.years_experience = request_body["years_experience"]
    user.include_name_salary = request_body["include_name_salary"]

    if request_body["password"] != user.password:
        password = request_body["password"]
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user.password = pw_hash

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
