from flask import request
from flask_restful import Resource

from app import db
from app.models import User
from .schema import UserSchema, UserRegisterSchema
from ..auth.jwt_utils import JWTUtils


class UsersResource(Resource):
    @JWTUtils.verify_token
    def get(self):
        schema = UserSchema(many=True)
        users = User.query.all()
        return schema.dump(users), 200

    @JWTUtils.verify_token
    def post(self):
        schema = UserRegisterSchema()
        user = schema.load(request.json)

        db.session.add(user)
        db.session.commit()

        return schema.dump(user), 201


class UserResource(Resource):
    @JWTUtils.verify_token
    def get(self, id):
        user = User.query.get_or_404(id)
        return UserSchema().dump(user), 200

    @JWTUtils.verify_token
    def put(self, id):
        schema = UserSchema()
        user = User.query.get(id)

        if not user:
            return {
                "message": "user not found"
            }, 404

        user = schema.load(request.json, instance=user)

        db.session.add(user)
        db.session.commit()

        return schema.dump(user)

    @JWTUtils.verify_token
    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {"message": f"{user.email} deleted"}, 204
