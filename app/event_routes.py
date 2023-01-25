from flask import Blueprint, request, jsonify, make_response, abort
from app import db
import os
import requests
from app.models.adie import Adie
from app.models.event import Event

event_bp = Blueprint('events', __name__, url_prefix="/events")