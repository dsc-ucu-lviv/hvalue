from flask import Blueprint, render_template, request, redirect, url_for

from web_server.login import users


registration_page = Blueprint('registration', __name__, template_folder='templates')


@registration_page.route("/", methods=["GET", "POST"])
def registration():
    if request.method == "POST":

        parameters = ["name", "email", "phone number", "password"]
        for parameter in parameters:
            if not request.form.get(parameter):
                error = 'enter {}'.format(parameter)
                return render_template('registration.html', error=error)

            if parameter == "name":
                users[request.form.get("name")] = []
            elif parameter != "name":
                users[request.form.get("name")].append(request.form.get(parameter))

        return redirect(url_for('login.hello'))

    return render_template("registration.html", error=False)



