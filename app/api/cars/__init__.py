from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from .controller import CarSaleResource, SingleCarSaleResource

api_cars_bp = Blueprint('api_cars', __name__)
api = Api(api_cars_bp, errors=api_cars_bp.app_errorhandler)
api.add_resource(CarSaleResource, "/")
api.add_resource(SingleCarSaleResource, "/<int:id>")


@api_cars_bp.app_errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
