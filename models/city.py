from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from config import db


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    country = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)

    country_object = relationship('Country')
    country_name = association_proxy('country_object', 'name')