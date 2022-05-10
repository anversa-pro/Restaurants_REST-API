from flask_jwt import jwt_required

from config import db
from flask import Blueprint, request
import bcrypt

from models.restaurant import Restaurant
from models.user import User
from validators.validator import Validator

user_blueprint = Blueprint('user_blueprint', __name__, url_prefix="/users")


@user_blueprint.route('/', methods=['POST'])
def create_user():
    try:
        body_json = request.json

        username = body_json.get('username') or ''
        email = body_json.get('email') or ''
        password_str = body_json.get('password') or ''

        create = Validator.validate(username, email, password_str)

        if create:
            password_hashed = bcrypt.hashpw(password_str.encode(), bcrypt.gensalt())

            new_user = User(username=username, password=password_hashed, email=email)

            db.session.add(new_user)
            db.session.commit()

            return {'message': f'user {new_user.username} has been created successfully'}, 202

        else:
            return {'message': 'some parameters are missing'}, 400

    except Exception as e:
        print(f'error en create_user(): {e}')
        return {'message': 'sorry, we are cooking :v'}, 500


@user_blueprint.route('/restaurants', strict_slashes=False)
@jwt_required()
def get_restaurant():
    try:
        args = request.args
        user_id = request.userid

        if args:
            if args.get('private'):
                private_restaurants = Restaurant.query.filter_by(public_access=False, user_id=user_id).all()
                return {'restaurant': [restaurant.to_json() for restaurant in private_restaurants]}, 200
        else:
            restaurants = Restaurant.query.filter_by(user_id=user_id).all()
            return {'restaurant': [restaurant.to_json() for restaurant in restaurants]}, 200
    except Exception as e:
        print(f'error en get_restaurant(): {e}')
        return {'message': 'sorry, we are cooking :v'}, 500
