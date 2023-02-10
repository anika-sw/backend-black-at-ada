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

auth_bp = Blueprint("", __name__, url_prefix="")

def validate_complete_new_user_request(request_body):
    try:
        if {
            request_body["first_name"],
            request_body["last_name"],
            request_body["cohort"],
            request_body["location_name"],
            request_body["email"],
            request_body["password"],
            request_body["profile_pic_url"],
            request_body["include_name_salary"]
            }:
            return request_body

    except:
        abort(make_response({"details": "Missing required data"}, 400))

    
def validate_new_user_email(cls, user_email):
    
    email_in_db = cls.query.filter_by(email=user_email).first()

    if not email_in_db:
        return user_email
    else:
        abort(make_response({"details": "Email already in use"}, 400)) 

def validate_complete_login_request(request_body):
    if request_body["email"] and request_body["password"]:
        return request_body

    abort(make_response({"details": "Missing email or password"}, 400))


def validate_returning_user(cls, user_email):
    user_in_db = cls.query.filter_by(email=user_email).first()

    if not user_in_db:
        abort(make_response({"details": "User not found"}, 404))
    
    return user_in_db


@auth_bp.route("/signup", methods=["POST"])
def create_user():
    request_body = request.get_json()
    valid_data = validate_complete_new_user_request(request_body)
    valid_email = validate_new_user_email(User, request_body["email"])
    password = valid_data["password"]
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    valid_data["email"] = valid_email
    valid_data["password"] = pw_hash
    new_user = User.from_dict(valid_data)

    db.session.add(new_user)
    db.session.commit()

    user_response = {
        "user": new_user.to_dict()
    }
    return make_response(jsonify(user_response), 201)  

@auth_bp.route("/login", methods=["POST"])
def user_login(): 
    request_body = request.get_json()
    valid_data = validate_complete_login_request(request_body)
    valid_user = validate_returning_user(User, valid_data["email"])    

    if bcrypt.check_password_hash(valid_user.password, valid_data["password"]):
        return jsonify(valid_user.id)
    else:
        return "Incorrect password"


    
    
    
    
    
    
    
    
