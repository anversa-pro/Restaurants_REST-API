from flask import Blueprint
from flask_jwt import jwt_required

from config import db
from models.country import Country


country_blueprint = Blueprint('country_blueprint', __name__, url_prefix="/countries")


@country_blueprint.route('/')
@jwt_required()
def get_countries():
    try:
        countries = Country.query.all()
        if countries:
            # for country in countries:
            #    json_result = {'countries': country.to_json()}
            # return json_result, 200
            return {'countries': [country.to_json() for country in countries]}, 200
        else:
            return {'message': 'sorry, we have no countries to visit :v'}, 404

    except Exception as e:
        print(f'error en get_countries(): {e}')
        return {'message': 'sorry, we are cooking :v'}, 500


@country_blueprint.route('/<country_id>')
@jwt_required()
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
