from flask import request

from . import auth_bp
from app.api.auth.jwt_utils import JWTUtils
from app.models import User


@auth_bp.route('/login', methods=['POST'])
def login_post():
    data = request.json
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return {"error": "Invalid credentials"}
    return {"token": JWTUtils.create_token(username=username)}