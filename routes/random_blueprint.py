import requests as requests
from flask import Blueprint

random_blueprint = Blueprint('random_blueprint', __name__, url_prefix="/random")


@random_blueprint.route('/')
def get_random_number():

    url = 'http://www.randomnumberapi.com/api/v1.0/random'
    query = '?min=100&max=1000&count=5'

    try:
        r = requests.get(url+query)
        result = {'random number': r.text}
        return result, 200

    except Exception as e:
        print(f'error en get_random_number(): {e}')
        return {f'message': 'sorry, we are calculating :v'}, 500
