from flask import Flask, render_template, request, redirect, Blueprint
from models.city import City
from models.country import Country
from app import db

city_blueprint = Blueprint("cities", __name__)

@city_blueprint.route("/cities")
def get_cities():
    cities_from_db = City.query.all()
    countries_from_db = Country.query.all()
    return render_template("base.jinja", cities=cities_from_db, countries=countries_from_db)