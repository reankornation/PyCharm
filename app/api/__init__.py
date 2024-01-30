from flask import Blueprint

api_bp = Blueprint('api', __name__)

from .jobs import api_jobs_bp
api_bp.register_blueprint(api_jobs_bp, url_prefix="/jobs")

from . import controller