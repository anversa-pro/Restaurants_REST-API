import datetime
import os
from dotenv import load_dotenv
from flasgger import Swagger

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}' \
                                        f'@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
app.config['SECRET_KEY'] = os.environ["JWT_SECRET_KEY"]
app.config['JWT_AUTH_USERNAME_KEY'] = "email"
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(minutes=20)
app.config['SWAGGER'] = {'title': 'RESTAURANT RESTFUL API',
                         'description': 'HTTP server REST API implementation for the best restaurants in LATAM'}

swagger = Swagger(app)

db = SQLAlchemy(app)
