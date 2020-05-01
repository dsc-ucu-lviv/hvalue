from flask import Blueprint, render_template, request, redirect, url_for

from database.db import db
import database.db_base as db_error
import database.db

login_page = Blueprint('login', __name__, template_folder='templates')


@login_page.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("email"):
            try:
                user_id = db.db_users.check_user_password_by_email(request.form.get("email"),
                                                                  request.form.get("password"))
                if user_id:
                    database.db.profile_info = db.db_users.get_general_user_info(user_id)
                    database.db.profile_info['user_id'] = user_id
                    return redirect(url_for('map.map'))
                else:
                    error = 'enter right password'
                    return render_template('login.html', error=error)
            except db_error.UserDoesNotExists:
                error = 'user does not exist'
                return render_template('login.html', error=error)
        else:
            error = 'enter right username'
            return render_template('login.html', error=error)

    return render_template("login.html")


@login_page.route("/log_out", methods=["GET"])
def log_out():
    database.db.profile_info = None
    return redirect(url_for('map.map'))
