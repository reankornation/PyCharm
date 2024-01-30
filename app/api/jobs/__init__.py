from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from .controller import JobResource, SingleJobResource

api_jobs_bp = Blueprint('api_jobs', __name__)
api = Api(api_jobs_bp, errors=api_jobs_bp.app_errorhandler)
api.add_resource(JobResource, "/jobs")
api.add_resource(SingleJobResource, "/jobs/<int:id>")


@api_jobs_bp.app_errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400