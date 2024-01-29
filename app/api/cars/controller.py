from flask import request
from flask_restful import Resource

from app import db
from app.api.cars.models import CarSale
from app.api.cars.schemas import CarSaleSchema


class CarSaleResource(Resource):
    def get(self):
        schema = CarSaleSchema(many=True)
        car_sales = CarSale.query.all()
        return schema.dump(car_sales), 200

    def post(self):
        schema = CarSaleSchema()
        car = schema.load(request.json)

        db.session.add(car)
        db.session.commit()

        return schema.dump(car)


class SingleCarSaleResource(Resource):
    def get(self, id):
        car_sale = CarSale.query.get_or_404(id)
        return CarSaleSchema().dump(car_sale), 200

    def put(self, id):
        schema = CarSaleSchema()
        car = CarSale.query.get(id)

        if not car:
            return {
                "message": "car not found"
            }, 404

        car = schema.load(request.json, instance=car)

        db.session.add(car)
        db.session.commit()

        return schema.dump(car)

    def delete(self, id):
        car_sale = CarSale.query.get_or_404(id)
        db.session.delete(car_sale)
        db.session.commit()
        return {"message": f"Car {car_sale.make} {car_sale.model} deleted"}, 200
