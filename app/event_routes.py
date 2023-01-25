from flask import Blueprint, request, jsonify, make_response, abort
from app import db
import os
import requests
from app.models.user import User
from app.models.event import Event

events_bp = Blueprint('events', __name__, url_prefix="/events")