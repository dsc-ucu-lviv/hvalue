from flask import Blueprint, render_template, request, redirect, url_for

import database.db

profile_org_page = Blueprint('profile_org', __name__, template_folder='templates')


@profile_org_page.route("/profile_org", methods=["GET", "POST"])
def profile_org():
    if request.method == "POST":
        return "good"

    org = {'org_name': database.db.profile_info['username'], 'org_type': None, 'num_stations': None,
           'phone_number': None, 'email': database.db.profile_info['email']}

    return render_template("profile_org.html", org=org)
    # return render_template("profile_org.html", org_name="Myloserd", org_type="Prytuloc",
    #                        num_stations=9, phone_number=999, email="denys@gmail", name_stations=["Prutuloc1",
    #                                                                                              "Prutuloc2"],
    #                        categories=["food", "sleep"], addresses=["UCU", "ucu2"])
