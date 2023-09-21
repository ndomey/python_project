from flask import Flask, render_template, request, redirect, Blueprint
from models.city import City
from models.country import Country
from app import db

# you will want to split this file into two separate files, a 'city controller' and a 'country controller' 
# This will help keep our code organised, the controller functions that handle requests about cities will live in the city controller, and the same for the countries. 

# our routes are not restful here, to follow the restful convention we would need to have each resource using separate endpoints(url) and should follow a consistent and meaningful structure, for example

#    - `GET /countries`: Retrieve a list of all countries.
#    - `POST /countries`: Create a new country.
#    - `GET /countries/{id}`: Retrieve a specific country by its ID.
#    - `PUT /countries/{id}` or `PATCH /countries/{id}`: Update a specific country by its ID.
#    - `DELETE /countries/{id}`: Delete a specific country by its ID.

# In this example we are using all the HTTP verbs, which we don't have the ability to use without JavaScript, so can't be fully RESTful in how we structure our endpoints. 

# In RESTful routing, resources represent entities or objects within your application, e.g the instances of our classes and the tables in our database. 

# so for your app, endpoints(urls) to do with countries start with "/countries"

# and endpoints(urls) to do with cities should start with "/cities"





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


# what happens when we have two cities in the same country with the same name? 
# as a rule of thumb we should not use non-unique things like names to delete from our database, we should only use things that are confirmed unique like our ID's  
@city_blueprint.route("/countries/<id>/<city_name>/delete", methods=["POST"])
def delete_city(id, city_name):
    City.query.filter_by(country_id = id, city_name=city_name).delete()
    db.session.commit()
    return redirect("/countries/" + id)


# we don't need to send the country ID in our request here, it's uneeded, even if we want to redirect to that country ID we can use the city.country_id to do this. 
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