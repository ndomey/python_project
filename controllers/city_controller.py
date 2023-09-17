from flask import Flask, render_template, request, redirect, Blueprint
from models.city import City
from models.country import Country
from app import db

city_blueprint = Blueprint("cities", __name__)