from sqlalchemy import func
from flask import Flask, Blueprint, request, jsonify, make_response, abort
from app import db
import os
import uuid
import requests
from app.models.user import User
from app.models.event import Event
from google.cloud import storage


image_bp = Blueprint("images", __name__, url_prefix="/images")

@image_bp.route("/upload", methods=["POST"])
def upload_image_to_cloud_storage():
    uploaded_file = request.files.get("image")
    org_filename = uploaded_file.filename
    storage_client = storage.Client.from_service_account_json("image_upload_sa.json")
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
