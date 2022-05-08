import os
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}' \
                                        f'@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
app.config['SECRET_KEY'] = 'super-secret'

db = SQLAlchemy(app)
