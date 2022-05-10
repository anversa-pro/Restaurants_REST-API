from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from config import db
from models.city import City


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    ranking = db.Column(db.Integer, nullable=False, unique=True)
    chef = db.Column(db.String(200), nullable=False)
    abstract = db.Column(db.String(1023), nullable=False)
    public_access = db.Column(db.Boolean, nullable=False)
    city = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    city_two = relationship('City')
    city_name = association_proxy('city_two', 'name')

    def to_json(self):
        dictionary = self.__dict__.copy()
        dictionary.pop('_sa_instance_state')
        return dictionary
