import os
import uuid
import requests
import json
from sqlalchemy import func
from flask import Flask, Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.user import User
from app.models.event import Event
from google.cloud import storage
from google.oauth2 import service_account

image_bp = Blueprint("images", __name__, url_prefix="/images")

@image_bp.route("/upload", methods=["POST"])
def upload_image_to_cloud_storage():
    creds_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    creds_info = json.loads(creds_json)
    credentials = service_account.Credentials.from_service_account_info(creds_info)
    storage_client = storage.Client(credentials=credentials)
    uploaded_file = request.files.get("image")
    org_filename = uploaded_file.filename
    bucket_name = os.environ.get("GCP_STORAGE_BUCKET_NAME")
    bucket = storage_client.bucket(bucket_name)
    file_extension = org_filename.split('.').pop()
    unique_id = str(uuid.uuid4())
    new_file_name = f"{unique_id}.{file_extension}"
    blob = bucket.blob(new_file_name) 
    blob.content_type = uploaded_file.content_type
    blob.upload_from_file(uploaded_file)

    image_response = {
        "url": blob.public_url
    }
    
    return make_response(jsonify(image_response), 201) 
