from flask import Blueprint, render_template, request, redirect, url_for

login_page = Blueprint('login', __name__, template_folder='templates')

# the dictionary will be look like this
users = {}


@login_page.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("name") in users:
            if request.form.get("password") == users[request.form.get("name")]["password"]:
                return redirect(url_for('login.hello'))
            else:
                error = 'enter right password'
                return render_template('login.html', error=error)
        else:
            error = 'enter right username'
            return render_template('login.html', error=error)

    return render_template("login.html")


@login_page.route("/hello", methods=['GET'])
def hello():
    return render_template("hello.html")