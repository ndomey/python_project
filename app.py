from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost:5432/travel_app"
db = SQLAlchemy(app)

from models.city import City
from models.country import Country

migrate = Migrate(app, db)

from controllers.city_controller import city_blueprint

app.register_blueprint(city_blueprint)

@app.route("/")
def home():
  return "This is the home page!"