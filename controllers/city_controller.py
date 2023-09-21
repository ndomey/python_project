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
    return redirect("/countries/" + id)


@city_blueprint.route("/countries/<id>/delete", methods=["POST"])
def delete_country(id):
    if City.query.filter_by(country_id = id).first():
        return render_template("error.jinja")
    else:
        Country.query.filter_by(id = id).delete()
        db.session.commit()
        return redirect('/countries')

# @city_blueprint.route("/countries/<id>/delete", methods=["POST"])    #use this at your own risk
# def delete_country(id):
#     country = Country.query.filter_by(id = id).first()
#     City.query.filter_by(country_id = id).delete()
#     db.session.delete(country)
#     db.session.commit()
#     return redirect('/countries')


@city_blueprint.route("/countries/<id>/<city_name>/delete", methods=["POST"])
def delete_city(id, city_name):
    City.query.filter_by(country_id = id, city_name=city_name).delete()
    db.session.commit()
    return redirect("/countries/" + id)


@city_blueprint.route("/countries/<country_id>/<city_id>/update", methods=["POST"])
def update_visited_status(country_id, city_id):
    if "checked_out" in request.form:
        city = City.query.get(city_id)
        city.visited = True
        db.session.commit()
    else:
        city = City.query.get(city_id)
        city.visited = False
        db.session.commit()
    return redirect("/countries/" + country_id)

@city_blueprint.route("/search")
def search():
    return render_template("page_not_found.jinja")