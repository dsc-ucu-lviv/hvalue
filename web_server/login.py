from flask import Blueprint, render_template, request, redirect, url_for

from database.db import db
import database.db_base as db_error

login_page = Blueprint('login', __name__, template_folder='templates')


@login_page.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("email"):
            try:
                if db.db_users.check_user_password_by_email(request.form.get("email"),
                                                            request.form.get("password")):
                    return redirect(url_for('login.hello'))
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


@login_page.route("/hello", methods=['GET'])
def hello():
    return render_template("hello.html")
