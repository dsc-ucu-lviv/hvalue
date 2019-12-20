from flask import Blueprint, render_template, request, redirect, url_for

login_page = Blueprint('login', __name__, template_folder='templates')

users = {'sofiia': '123'}


@login_page.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("name") in users:
            print('user is ok')
            if request.form.get("password") == users[request.form.get("name")]:
                print('password is ok')
                return redirect(url_for('login.hello'))
            else:
                print('password not ok')
                error = 'enter password'
                return render_template('login.html', error=error)
        else:
            print('user is not ok')
            error = 'enter right username'
            return render_template('login.html', error=error)

    return render_template("login.html")


@login_page.route("/hello", methods=['GET'])
def hello():
    return render_template("hello.html")
