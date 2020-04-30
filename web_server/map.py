from flask import Blueprint, render_template, request, redirect, url_for
import json
import database.db

map_page = Blueprint('map', __name__, template_folder='templates')


@map_page.route("/map", methods=["GET", "POST"])
def map():

    print("receiver_type_0" in request.form)
    companies_information = [{"organization_name": "UCU", "lat": 49.817731, "lng": 24.023823,
                              "needs": 'meal', "url": 'https://cms.ucu.edu.ua/course/view.php?id=2348'},
                             {"organization_name": "UCU Colegium", "lat": 49.818160, "lng": 24.022621,
                              "needs": 'help', "url": 'https://cms.ucu.edu.ua/course/view.php?id=2348'}]

    return render_template("map.html", coords=companies_information,
                           city_center_coords={"lat": 49.8397, "lng": 24.0297},
                           profile_info=database.db.profile_info)
