from flask import Blueprint, render_template, request, redirect, url_for
import json
from database.db import db
import database.db

map_page = Blueprint('map', __name__, template_folder='templates')


@map_page.route("/map", methods=["GET", "POST"])
def map():
    if request.method == "POST":
        matched_stations = db.db_map.get_easy_rcv_station({
            'city': request.form.get("city_input"),
            'station_type': request.form.getlist("station_type"),
            'time_from': "01-01-2018",
            'time_to': "01-01-2021",
            'organizations': request.form.getlist("organization"),
            'categories': request.form.getlist("donation")
        })

        return render_template("map.html", coords=matched_stations,
                               city_center_coords={"lat": 49.8397, "lng": 24.0297},
                               profile_info=database.db.profile_info)

    sample_stations = [{"organization_name": "UCU", "lat": 49.817731, "lng": 24.023823,
                              "needs": 'meal', "url": 'https://cms.ucu.edu.ua/course/view.php?id=2348'},
                             {"organization_name": "UCU Colegium", "lat": 49.818160, "lng": 24.022621,
                              "needs": 'help', "url": 'https://cms.ucu.edu.ua/course/view.php?id=2348'}]

    return render_template("map.html", coords=sample_stations,
                           city_center_coords={"lat": 49.8397, "lng": 24.0297},
                           profile_info=database.db.profile_info)
