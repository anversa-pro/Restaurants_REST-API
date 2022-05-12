from flasgger import swag_from
from flask import Blueprint, request
from flask_jwt import jwt_required

from config import db
from models.city import City
from models.country import Country
from models.restaurant import Restaurant
from validators.validator import Validator

restaurant_blueprint = Blueprint('restaurant_blueprint', __name__, url_prefix="/restaurants")


@restaurant_blueprint.route('/')
@jwt_required()
@swag_from('../documentation/get_restaurants.yml')
def get_restaurants():
    try:
        args = request.args
        user_id = request.userid
        restaurants = Restaurant.query.filter_by(public_access=True).all()
        # Add relationship to city & country
        if args:
            if args.get('private'):
                private_restaurants = Restaurant.query.filter_by(public_access=False, user_id=user_id).all()
                for restaurant in private_restaurants:
                    restaurants.append(restaurant)
        return {'restaurant': [restaurant.to_json() for restaurant in restaurants]}, 200

    except Exception as e:
        print(f'error en get_restaurants(): {e}')
        return {'message': 'sorry, we are cooking :v'}, 500


@restaurant_blueprint.route('/<restaurant_id>')
@jwt_required()
def get_restaurant(restaurant_id=None):
    try:
        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant:
            if restaurant.public_access or request.userid == restaurant.user_id:
                json_result = {'restaurant': restaurant.to_json()}
                json_result['restaurant']['city_name'] = restaurant.city_name
                json_result['restaurant']['country_name'] = restaurant.city_two.country_name
                return json_result, 200
            return {'message': 'sorry, you are not the owner :v'}, 403
        else:
            return {'message': 'sorry, that restaurant does not exist :v'}, 404
    except Exception as e:
        print(f'error en get_restaurant(): {e}')
        return {'message': 'sorry, we are cooking :v'}, 500


@restaurant_blueprint.route('/create', methods=['POST'])
@jwt_required()
def create_restaurant():
    try:
        body_json = request.json

        name = body_json.get('name') or ''
        ranking = body_json.get('ranking') or ''
        chef = body_json.get('chef') or ''
        abstract = body_json.get('abstract') or ''
        access = body_json.get('public_access') or False
        city = body_json.get('city') or ''
        user_id = request.userid

        create = Validator.validate_nonempty(name, ranking, chef, abstract, access, city, user_id)

        if create:
            new_restaurant = Restaurant(name=name, ranking=ranking, chef=chef, abstract=abstract, public_access=access,
                                        city=city, user_id=user_id)

            db.session.add(new_restaurant)
            db.session.commit()

            return {'message': f'restaurant {new_restaurant.id} has been created successfully'}, 202

        else:
            return {'message': 'some parameters are missing'}, 400
    except Exception as e:
        print(f'error en create_restaurant(): {e}')
        return {'message': 'sorry, we are cooking :v'}, 500


@restaurant_blueprint.route('/<restaurant_id>/update', methods=['PUT'])
@jwt_required()
def update_restaurant(restaurant_id=None):
    try:
        body_json = request.json
        for key, value in body_json.items():
            if hasattr(Restaurant, key) is False:
                return {"message": f'sorry the attribute: {key}, does not exist '}, 400
        if Restaurant.query.get(restaurant_id):
            Restaurant.query.filter_by(id=restaurant_id).update(body_json)
            db.session.commit()
            return {'message': 'success'}, 200
        return {'message': 'sorry, invalid id'}, 400
    except Exception as e:
        print(f'error en get_restaurant(): {e}')
        return {'message': 'sorry, we are cooking :v'}, 500


@restaurant_blueprint.route('/<restaurant_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_restaurant(restaurant_id=None):
    try:
        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return {'message': 'success'}, 200
        return {'message': 'sorry, invalid id'}, 400
    except Exception as e:
        print(f'error en get_restaurant(): {e}')
        return {'message': 'sorry, we are cooking :v'}, 500
