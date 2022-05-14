import requests as requests
from flasgger import swag_from
from flask import Blueprint

random_blueprint = Blueprint('random_blueprint', __name__, url_prefix="/random")


@random_blueprint.route('/')
@swag_from('../documentation/get_random.yml')
def get_random_number():

    url = 'http://www.randomnumberapi.com/api/v1.0/random'
    query = '?min=10&max=100&count=5'

    try:
        r = requests.get(url+query)
        result = {'random numbers': r.text}
        return result, 200

    except Exception as e:
        print(f'error en get_random_number(): {e}')
        return {f'message': 'sorry, we are calculating :v'}, 500
