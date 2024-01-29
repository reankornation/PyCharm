from flask import Blueprint

authet_bp = Blueprint("authet", __name__, template_folder="templates")

from . import views