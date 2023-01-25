from flask import Blueprint, request, jsonify, make_response, abort
from app import db
import os
import requests
from app.models.event import event
from app.models.event import Event

events_bp = Blueprint('events', __name__, url_prefix="/events")

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


@events_bp.route("", methods=["POST"])
def create_event():
    request_body = request.get_json()
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
    events = Event.query.all()
    events_response = [event.to_dict() for event in events]

    return make_response(jsonify(events_response), 200)


@events_bp.route("/<event_id>", methods=["GET"])
def read_one_event(event_id):
    event = validate_model_id(event, event_id)
    event_response = {
        "event": event.to_dict()
    }
    return make_response(jsonify(event_response), 200)

@events_bp.route("/<event_id>", methods=["PUT"])
def update_event_entire_entry(event_id):
    event = validate_model_id(event, event_id)
    request_body = request.get_json()
    event.title = request_body["title"]
    event.description = request_body["description"]
    event.date = request_body["date"]
    event.time = request_body["time"]
    event.location = request_body["location"]
    event.organizer_first_name = request_body["organizer_first_name"]
    event.organizer_last_name = request_body["organizer_last_name"]
    event.organizer_email = request_body["organizer_email"]
    event.target_audience = request_body["target_audience"]

    db.session.commit()

    event_response = {
        "event": event.to_dict()
    }
    return make_response((event_response), 200)

@events_bp.route("/<event_id>", methods=["PATCH"])
def update_event_partial_entry(event_id):
    event = validate_model_id(event, event_id)
    request_body = request.get_json()
    event.title = request_body["title"]
    event.description = request_body["description"]
    event.date = request_body["date"]
    event.time = request_body["time"]
    event.location = request_body["location"]
    event.organizer_first_name = request_body["organizer_first_name"]
    event.organizer_last_name = request_body["organizer_last_name"]
    event.organizer_email = request_body["organizer_email"]
    event.target_audience = request_body["target_audience"]
    event.attendees = request_body["attendees"]

    db.session.commit()

    event_response = {
        "event": event.to_dict()
    }
    return make_response((event_response), 200)


@events_bp.route("/<event_id>", methods=["DELETE"])
def event_delete(event_id):
    event = validate_model_id(event, event_id)

    db.session.delete(event)
    db.session.commit()

    return make_response({'details': f'{event.title} successfully deleted'}, 200)