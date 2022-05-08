from flask import Blueprint
from flask_jwt import jwt_required

from models.restaurant import Restaurant

restaurant_blueprint = Blueprint('restaurant_blueprint', __name__, url_prefix="/restaurants")


@restaurant_blueprint.route('/')
@jwt_required()
def get_restaurants():
    try:
        restaurants = Restaurant.query.all()
        return {'restaurant': [restaurant.to_json() for restaurant in restaurants]}, 200
    except Exception as e:
        print(f'error en get_restaurant(): {e}')
        return {'message': 'sorry, we are cooking :v'}, 500
