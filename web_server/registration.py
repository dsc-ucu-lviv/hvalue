from flask import Blueprint, render_template, request, redirect, url_for

import database.db_auth as db_auth
from database.db import db


registration_page = Blueprint('registration', __name__, template_folder='templates')
parameters = ["name", "email", "password1", "password2"]


@registration_page.route("/", methods=["GET", "POST"])
def registration():
    if request.method == "POST":

        for parameter in parameters:
            if not request.form.get(parameter):
                error = 'enter {}'.format(parameter)
                return render_template('registration.html', error=error)

        if request.form.get("password1") != request.form.get("password2"):
            error = 'passwords do not match'
            return render_template('registration.html', error=error)

        if ('@' and '.') in request.form.get("email"):
            user_dict = {'email': request.form.get("email"),
                         'password': request.form.get("password1"),
                         'username': request.form.get("name")}

            try:
                db.db_auth.add_new_user(user_dict)
                return redirect(url_for("login.login"))
            except db_auth.UserAlreadyExists:
                error = 'user already exists'
                return render_template('login.html', error=error)

        else:
            error = 'enter right email'
            return render_template('login.html', error=error)

    return render_template("registration.html", error=False)
