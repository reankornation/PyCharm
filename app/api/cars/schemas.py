from datetime import datetime

from marshmallow import ValidationError, validates_schema, fields

from app import ma
from .models import CarSale


class CarSaleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = CarSale
        load_instance = True

    make = fields.String(required=True)
    model = fields.String(required=True)
    year = fields.Integer(required=True)
    price = fields.Float(required=True)
