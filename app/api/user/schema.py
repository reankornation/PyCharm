from marshmallow import fields, ValidationError, validates_schema

from app import ma
from ...models import User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
    about_me = fields.String(required=True)

    @validates_schema
    def validate_email(self, data, **kwargs):
        id = data.get('id')
        user = User.query.filter(User.email == data.get('email')).first()
        if user:
            if user.id != id:
                raise ValidationError("User with same email exists")

    @validates_schema
    def validate_username(self, data, **kwargs):
        id = data.get('id')
        user = User.query.filter(User.username == data.get('username')).first()
        if user:
            if user.id != id:
                raise ValidationError("User with same username exists")


class UserRegisterSchema(UserSchema):
    password = fields.String(required=True)