from flasgger import swag_from
from flask import Blueprint, request
from flask_jwt import jwt_required

from models.city import City
from config import db
from models.country import Country


city_blueprint = Blueprint('city_blueprint', __name__, url_prefix="/cities")


@city_blueprint.route('/')
@swag_from('../documentation/swagger.yaml')
@jwt_required()
def get_cities():
    try:
        args = request.args
        page = 1
        per_page = 5

        if args:
            try:
                page = int(args.get('page'))
                per_page = int(args.get('limit'))

                if (page < 0) or (per_page < 0):
                    return {'message': 'sorry, invalid pagination query arguments  :v'}, 400

            except Exception as e:
                print(f'error en get_page(): {e}')
                return {'message': 'sorry, invalid pagination query arguments  :v'}, 400

        cities = City.query.paginate(per_page=per_page, page=page, error_out=False)

        if cities:
            cities_list = []

            pagination = {'total cities': cities.total,
                          'total pages': cities.pages,
                          'current page': cities.page,
                          'next page available': cities.has_next,
                          'cities per page': cities.per_page}

            for city in cities.items:
                city_dict = city.to_json()
                city_dict['country_name'] = city.country_name
                cities_list.append(city_dict)

            return {'pagination': [pagination], 'cities': cities_list}, 200

        return {'message': 'sorry, we have no cities to visit :v'}, 404

    except Exception as e:
        print(f'error en get_cities(): {e}')
        return {'message': 'sorry, we are cooking :v'}, 500


@city_blueprint.route('/<city_id>')
@jwt_required()
@swag_from('../documentation/swagger.yaml')
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
