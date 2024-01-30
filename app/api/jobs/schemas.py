from marshmallow import fields

from app import ma
from .models import Job


class JobSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Job
        load_instance = True

    title = fields.String(required=True)
    description = fields.String(required=True)
    requirements = fields.String(required=True)
    salary = fields.Float(required=True)