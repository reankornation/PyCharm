from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from .views import UserResource, UsersResource

api_user_bp = Blueprint('api_user', __name__)
api = Api(api_user_bp, errors=api_user_bp.app_errorhandler)
api.add_resource(UsersResource, "/")
api.add_resource(UserResource, "/<int:id>")


@api_user_bp.app_errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
