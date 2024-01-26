from flask import Blueprint, request, jsonify, make_response, abort
from app import db
import os
import requests
from app.models.user import User
from app.models.event import Event
from datetime import datetime
from sqlalchemy.sql import func
import reverse_geocoder as rg

events_bp = Blueprint('events', __name__, url_prefix="/events")

def validate_complete_request(request_body):
    try:
        if "title" in request_body:
            print(request_body)
            return request_body

    except:
        abort(make_response({"details": "Missing required data"}, 400))


def validate_model_id(cls, model_id):
    try:
        model_id = int(model_id)    
    except:
        abort(make_response({"details": "Invalid data"}, 404))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details": "Invalid data"}, 404))
    
    return model


@events_bp.route("", methods=["POST"])
def create_event():
    request_body = request.get_json()
    print(request_body)
    valid_data = validate_complete_request(request_body)
    new_event = Event.from_dict(valid_data)

    db.session.add(new_event)
    db.session.commit()

    event_response = {
        "event": new_event.to_dict()
    }
    return make_response(jsonify(event_response), 201)


@events_bp.route("", methods=["GET"])
def read_all_events():
    event_query = Event.query.filter(Event.date_time_start >= func.now()).order_by(Event.date_time_start.asc())
    sort_query = request.args.get("sort")
    if sort_query == "dateTimeCreated":
        event_query = Event.query.order_by(Event.date_time_created.desc())
    if sort_query == "past":
        event_query = Event.query.filter(Event.date_time_start <= func.now()).order_by(Event.date_time_start.desc())


    events = event_query
    events_response = [event.to_dict() for event in events]

    return make_response(jsonify(events_response), 200)


@events_bp.route("/<event_id>", methods=["GET"])
def read_one_event(event_id):
    event = validate_model_id(Event, event_id)
    event_response = {
        "event": event.to_dict()
    }
    return make_response(jsonify(event_response), 200)

@events_bp.route("/<event_id>", methods=["PATCH"])
def update_event(event_id):
    event = validate_model_id(Event, event_id)
    request_body = request.get_json()

    event.title = request_body["title"]
    event.description = request_body["description"]
    event.image_url = request_body["image_url"]
    event.date_time_start = request_body["date_time_start"]
    event.date_time_stop = request_body["date_time_stop"]
    event.timezone = request_body["timezone"]
    event.video_conf_link = request_body["video_conf_link"]
    event.meeting_key = request_body["meeting_key"]
    event.online_in_person = request_body["online_in_person"]
    event.location_address = request_body["location_address"]
    event.location_lat = request_body["location_lat"]
    event.location_lng = request_body["location_lng"]
    event.organizer_first_name = request_body["organizer_first_name"]
    event.organizer_last_name = request_body["organizer_last_name"]
    event.organizer_pronouns = request_body["organizer_pronouns"]
    event.organizer_email = request_body["organizer_email"]
    event.target_audience = request_body["target_audience"]

    db.session.commit()

    event_response = {
        "event": event.to_dict()
    }
    return make_response((event_response), 200)


@events_bp.route("/<event_id>/users", methods=["POST"])
def user_rsvp_yes(event_id):
    event = validate_model_id(Event, event_id)
    request_body = request.get_json()

    user = validate_model_id(User, request_body["user_id"])
    event.users.append(user)
    db.session.commit()

    event_response = {
        "id": event.id,
        "attending": True,
        "total_rsvp": len(event.users)
    }
    print(event_response)

    return make_response(jsonify(event_response), 200)


@events_bp.route("/<event_id>/users", methods=["PATCH"])
def user_rsvp_no(event_id):
    event = validate_model_id(Event, event_id)
    request_body = request.get_json()

    user = validate_model_id(User, request_body["user_id"])
    event.users.remove(user)
    db.session.commit()

    event_response = {
        "id": event.id,
        "attending": False,
        "total_rsvp": len(event.users),
        "user_id": f'User {request_body["user_id"]} successfully removed from event'
    }
    return make_response(jsonify(event_response), 200)


# @events_bp.route("/<event_id>/locale", methods=["GET"])
# def get_event_locale(event_id):
#     event = validate_model_id(Event, event_id)

#     lat = float(event.location_lat)
#     lng = float(event.location_lng)

#     coordinates = (lat, lng)
#     results = rg.search(coordinates)

#     return {"locale": tuple(results)}


@events_bp.route("/<event_id>", methods=["DELETE"])
def event_delete(event_id):
    event = validate_model_id(Event, event_id)

    db.session.delete(event)
    db.session.commit()

    return make_response({'details': f'{event.title} successfully deleted'}, 200)