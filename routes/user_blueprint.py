from config import db
from flask import Blueprint, request
import bcrypt

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

            return {'message': f'user {new_user.id} has been created successfully'}, 202

        else:
            return {'message': 'some parameters are missing'}, 400

    except Exception as e:
        print(f'error en create_event(): {e}')
        return {'message': 'sorry, we are learning :v'}, 500
