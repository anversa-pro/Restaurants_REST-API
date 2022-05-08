from config import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

    restaurant_created = db.relationship('Restaurant', backref='user')
