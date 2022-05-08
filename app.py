from flask_jwt import JWT
from flask_sqlalchemy import SQLAlchemy

from config import app, db

from models.user import User
from models.restaurant import Restaurant
from models.city import City
from models.country import Country

from security.security import authenticate, identity

from routes.restaurant_blueprint import restaurant_blueprint
from routes.user_blueprint import user_blueprint

jwt = JWT(app, authenticate, identity)

app.register_blueprint(restaurant_blueprint)
app.register_blueprint(user_blueprint)

if __name__ == "__main__":
    db.create_all()
    app.run(port=8000, debug=True)
