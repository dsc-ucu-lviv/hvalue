from flask import Blueprint, render_template, request, redirect, url_for
import json

map_page = Blueprint('map', __name__, template_folder='templates')


@map_page.route("/map", methods=["GET", "POST"])
def map():
    companies_information = [{"company_title": "UCU", "lat": 24.023845, "lng": 49.817744,
                              "description": '<div id=\"content\">'+
                                '<div id=\"siteNotice\">'+
                                '</div>'+
                                '<h1 id=\"firstHeading\" class=\"firstHeading\">Uluru</h1>'+
                                '<div id=\"bodyContent\">'+
                                '<p><b>Uluru</b>, also referred to as <b>Ayers Rock</b>, is a large ' +
                                'sandstone rock formation in the southern part of the '+
                                'Northern Territory, central Australia. It lies 335&#160;km (208&#160;mi) '+
                                'south west of the nearest large town, Alice Springs; 450&#160;km '+
                                '(280&#160;mi) by road. Kata Tjuta and Uluru are the two major '+
                                'features of the Uluru - Kata Tjuta National Park. Uluru is '+
                                'sacred to the Pitjantjatjara and Yankunytjatjara, the '+
                                'Aboriginal people of the area. It has many springs, waterholes, '+
                                'rock caves and ancient paintings. Uluru is listed as a World '+
                                'Heritage Site.</p>'+
                                '<p>Attribution: Uluru, <a href=\"https://en.wikipedia.org/w/index.php?title=Uluru&oldid=297882194\">'+
                                'https://en.wikipedia.org/w/index.php?title=Uluru</a> '+
                                '(last visited June 22, 2009).</p>'+
                                '</div>'},
                             {"company_title": "Church", "lat": 25.023845, "lng": 49.817744,
                              "description": '<div id=\"content\">'+
                                  '<div id=\"siteNotice\">'+
                                  '</div>'+
                                  '<h1 id=\"firstHeading\" class=\"firstHeading\">Uluru</h1>'+
                                  '<div id=\"bodyContent\">'+
                                  '<p><b>Uluru</b>, also referred to as <b>Ayers Rock</b>, is a large ' +
                                  'sandstone rock formation in the southern part of the '+
                                  'Northern Territory, central Australia. It lies 335&#160;km (208&#160;mi) '+
                                  'south west of the nearest large town, Alice Springs; 450&#160;km '+
                                  '(280&#160;mi) by road. Kata Tjuta and Uluru are the two major '+
                                  'features of the Uluru - Kata Tjuta National Park. Uluru is '+
                                  'sacred to the Pitjantjatjara and Yankunytjatjara, the '+
                                  'Aboriginal people of the area. It has many springs, waterholes, '+
                                  'rock caves and ancient paintings. Uluru is listed as a World '+
                                  'Heritage Site.</p>'+
                                  '<p>Attribution: Uluru, <a href=\"https://en.wikipedia.org/w/index.php?title=Uluru&oldid=297882194\">'+
                                  'https://en.wikipedia.org/w/index.php?title=Uluru</a> '+
                                  '(last visited June 22, 2009).</p>'+
                                  '</div>'}]

    lat = -25.344
    lng = 131.036
    return render_template("map.html", coords=companies_information)
