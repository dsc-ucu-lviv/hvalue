from flask import Blueprint, render_template, request, redirect, url_for
import json

map_page = Blueprint('map', __name__, template_folder='templates')


@map_page.route("/map", methods=["GET", "POST"])
def map():
    companies_information = [{"organization_name": "UCU", "lat": 24.023845, "lng": 49.817744,
                              "needs": 'meal', "url": 'https://cms.ucu.edu.ua/course/view.php?id=2348'},
                             {"organization_name": "UCU Colegium", "lat": 25.023845, "lng": 50.817744,
                              "needs": 'help', "url": 'https://cms.ucu.edu.ua/course/view.php?id=2348'}]

    lat = -25.344
    lng = 131.036
    return render_template("map.html", coords=companies_information)
