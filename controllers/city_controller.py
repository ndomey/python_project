from flask import Flask, render_template, request, redirect, Blueprint
from models.city import City
from models.country import Country
from app import db



city_blueprint = Blueprint("countries", __name__)


@city_blueprint.route("/")
def home():
   return render_template("homepage.jinja")
   

@city_blueprint.route("/countries")
def get_countries():
    cities_from_db = City.query.all()
    countries_from_db = Country.query.all()
    return render_template("countries.jinja", cities=cities_from_db, countries=countries_from_db)


@city_blueprint.route("/countries/<id>")
def get_cities(id):
    cities = City.query.filter(City.country_id == id)
    selected_country = Country.query.get(id)
    return render_template("cities.jinja", cities=cities, country=selected_country)


@city_blueprint.route("/countries/new", methods=["POST"])
def add_country():
    name = request.form["name"]
    country = Country(name=name)
    db.session.add(country)
    db.session.commit()
    return redirect("/countries")


@city_blueprint.route("/countries/<id>/new", methods=["POST"])
def add_city(id):
    city_name = request.form["city_name"]
    country_id = id
    city = City(city_name=city_name, country_id=country_id)
    db.session.add(city)
    db.session.commit()
    return redirect("/countries/<id>")


@city_blueprint.route("/countries/<id>/delete", methods=["POST"])
def delete_country(id):
    Country.query.filter_by(id = id).delete()
    db.session.commit()
    return redirect('/country')