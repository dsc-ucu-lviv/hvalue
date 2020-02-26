from flask import Blueprint, render_template, request, redirect, url_for

import database.db_auth as db_auth

login_page = Blueprint('login', __name__, template_folder='templates')

from database.db import db


@login_page.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("email"):
            user_dict = {"email": request.form.get("email"),
                         "password": request.form.get("password")}
            try:
                if db.db_auth.check_user_password(user_dict) is not None:
                    return redirect(url_for('login.hello'))
                else:
                    error = 'enter right password'
                    return render_template('login.html', error=error)
            except db_auth.UserDoesNotExists:
                error = 'user does not exist'
                return render_template('login.html', error=error)
        else:
            error = 'enter right username'
            return render_template('login.html', error=error)

    return render_template("login.html")


@login_page.route("/hello", methods=['GET'])
def hello():
    return render_template("hello.html")