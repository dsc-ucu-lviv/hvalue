from flask import Blueprint, render_template, request, redirect, url_for
import database.db


profile_org_page = Blueprint('profile_org', __name__, template_folder='templates')


@profile_org_page.route("/profile_org", methods=["GET", "POST"])
def profile_org():
    if request.method == "POST":
        return "good"


    #     :param user_id:
    #     :return: (dict) {'username': str, 'phone_number': str / None, 'email': str,
    #     'stations': [{'name': str, 'address': str, 'categories': ['food' ... ]}]}
    #     """
    print(database.db.profile_info)

    if database.db.profile_info is not None:
        org_stations = database.db.db.db_station.get_profile_info(database.db.profile_info["user_id"]) or []
        org_profile = {'org_name': database.db.profile_info['username'],
                       'org_type': database.db.profile_info['type_id'],
                       'email': database.db.profile_info.get('email'),
                       'phone_number': database.db.profile_info.get('phone_number'),
                       'num_stations': len(org_stations) if org_stations else 0,
                       }
        print(database.db.db.db_station.get_profile_info(9))
        return render_template("profile_org.html", org=org_profile, stations=org_stations)

    return "R"


    #


    # return render_template("profile_org.html", org_name="Myloserd", org_type="Prytuloc",
    #                        num_stations=9, phone_number=999, email="denys@gmail", name_stations=["Prutuloc1",
    #                                                                                              "Prutuloc2"],
    #                        categories=["food", "sleep"], addresses=["UCU", "ucu2"])
