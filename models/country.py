from config import db


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def to_json(self):
        dictionary = self.__dict__.copy()
        dictionary.pop('_sa_instance_state')
        return dictionary