from config import app, db

from models.user import User
from models.restaurant import Restaurant
from models.city import City
from models.country import Country


@app.route('/')
def home():
    return "hello world"


if __name__ == "__main__":
    db.create_all()
    app.run(port=8000)
