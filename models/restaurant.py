from config import db


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    ranking = db.Column(db.Integer, nullable=False, unique=True)
    chef = db.Column(db.String(200), nullable=False)
    abstract = db.Column(db.String(1023), nullable=False)
    access = db.Column(db.Boolean, nullable=False)
    city = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

