from flask import Blueprint, render_template, request, redirect, url_for
import json

map_page = Blueprint('ma', __name__, template_folder='templates')


@map_page.route("/map", methods=["GET", "POST"])
def map():
    lat = -25.344
    lng = 131.036
    return render_template("map.html", coords=json.dumps({"lat": lat, "lng": lng}))
