import bcrypt
from flask import request

from models.user import User


def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.checkpw(password.encode(), user.password.encode()):
        return user


def identity(payload):
    user_id = payload['identity']
    setattr(request, "userid", {user_id})
    return User.query.get(user_id)

