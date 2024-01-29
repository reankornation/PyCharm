from flask import Blueprint

from .user import api_user_bp

api_bp = Blueprint('api', __name__)

from .auth import auth_bp
from .cars import api_cars_bp

api_bp.register_blueprint(api_cars_bp, url_prefix="/cars")
api_bp.register_blueprint(auth_bp, url_prefix="/auth")
api_bp.register_blueprint(api_user_bp, url_prefix="/user")

from . import controller
