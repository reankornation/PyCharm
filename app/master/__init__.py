from flask import Blueprint

master_bp = Blueprint("master", __name__, template_folder="templates")

from . import views