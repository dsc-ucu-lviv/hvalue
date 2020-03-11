from flask import Blueprint, render_template, request, redirect, url_for

from web_server.login import users


registration_page = Blueprint('registration', __name__, template_folder='templates')
parameters = ["name", "email", "phone number", "password"]


@registration_page.route("/", methods=["GET", "POST"])
def registration():
    if request.method == "POST":

        for parameter in parameters:
            if not request.form.get(parameter):
                error = 'enter {}'.format(parameter)
                return render_template('registration.html', error=error)

            if parameter == "name":
                users[request.form.get("name")] = {}
            elif parameter != "name":
                users[request.form.get("name")][parameter] = request.form.get(parameter)
        print(users)
        return redirect(url_for('login.hello'))

    return render_template("registration.html", error=False)
