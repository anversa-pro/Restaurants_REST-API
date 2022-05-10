from flask import Blueprint
from flask_jwt import jwt_required

from models.city import City
from config import db
from models.country import Country


city_blueprint = Blueprint('city_blueprint', __name__, url_prefix="/cities")


@city_blueprint.route('/')
@jwt_required()
def get_cities():
    try:
        cities = City.query.all()
        my_list = []
        if cities:
            for city in cities:
                my_dict = {city.id: city.to_json()}
                my_dict[city.id]['country_name'] = city.country_name
                my_list.append(my_dict)
            return {'cities': my_list}, 200
        else:
            return {'message': 'sorry, we have no cities to visit :v'}, 404

    except Exception as e:
        print(f'error en get_cities(): {e}')
        return {'message': 'sorry, we are cooking :v'}, 500


@city_blueprint.route('/<city_id>')
@jwt_required()
def get_city(city_id=None):
    try:
        city = City.query.get(city_id)
        if city:
            json_result = {'city': city.to_json()}
            json_result['city']['country_name'] = city.country_name
            return json_result, 200

        else:
            return {'message': f'sorry, the city id {city_id} does not exist :v'}, 404

    except Exception as e:
        print(f'error en get_city(): {e}')
        return {'message': 'sorry, we are cooking :v'}, 500
