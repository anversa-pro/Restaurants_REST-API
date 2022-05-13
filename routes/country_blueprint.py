from flasgger import swag_from
from flask import Blueprint, request
from flask_jwt import jwt_required

from config import db
from models.country import Country

country_blueprint = Blueprint('country_blueprint', __name__, url_prefix="/countries")


@country_blueprint.route('/')
@jwt_required()
@swag_from('../documentation/swagger.yaml')
def get_countries():
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

        countries = Country.query.paginate(per_page=per_page, page=page, error_out=False)

        if countries:
            pagination = {'total countries': countries.total,
                          'total pages': countries.pages,
                          'current page': countries.page,
                          'next page available': countries.has_next,
                          'countries per page': countries.per_page}

            return {'pagination': [pagination],
                    'countries': [country.to_json() for country in countries.items]}, 200

        return {'message': 'sorry, we have no countries to visit :v'}, 404

    except Exception as e:
        print(f'error en get_countries(): {e}')
        return {'message': 'sorry, we are cooking :v'}, 500


@country_blueprint.route('/<country_id>')
@jwt_required()
@swag_from('../documentation/swagger.yaml')
def get_country(country_id=None):
    try:
        country = Country.query.get(country_id)

        if country:
            return {'country': country.to_json()}, 200
        else:
            return {'message': f'sorry, the country id {country_id} does not exist :v'}, 404

    except Exception as e:
        print(f'error en get_country(): {e}')
        return {'message': 'sorry, we are cooking :v'}, 500
