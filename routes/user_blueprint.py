from flask_jwt import jwt_required

from config import db
from flask import Blueprint, request
import bcrypt

from models.restaurant import Restaurant
from models.user import User
from validators.user_validator import NewUser, UserNotValidError
from validators.validator import Validator
from validators.password_validator import Password, PasswordNotValidError

from email_validator import validate_email, EmailNotValidError

user_blueprint = Blueprint('user_blueprint', __name__, url_prefix="/users")


@user_blueprint.route('/', methods=['POST'])
def create_user():
    try:
        body_json = request.json

        username = body_json.get('username') or ''
        email = body_json.get('email') or ''
        password_str = body_json.get('password') or ''

        non_empty = Validator.validate_nonempty(username, email, password_str)

        if non_empty:
            try:
                NewUser.validate_new_user(username, email)
            except UserNotValidError as e:
                return{'message': f'sorry, {e}'}, 400

            try:
                validate_email(email).email
            except EmailNotValidError as e:
                return {'message': f'sorry, {e}'}, 400

            try:
                Password.validate_password(password_str)
            except PasswordNotValidError as e:
                return {'message': f'sorry, {e}'}, 400

            password_hashed = bcrypt.hashpw(password_str.encode(), bcrypt.gensalt())

            new_user = User(username=username, password=password_hashed, email=email)

            db.session.add(new_user)
            db.session.commit()

            return {'message': f'user {new_user.username} has been created successfully'}, 202

        else:
            return {'message': 'some parameters are missing'}, 400

    except Exception as e:
        print(f'error en create_user(): {e}')
        return {f'message': 'sorry, we are cooking :v'}, 500


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
