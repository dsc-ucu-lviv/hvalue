from flask import Blueprint, render_template, request, redirect, url_for

from web_server.login import users


registration_page = Blueprint('registration', __name__, template_folder='templates')


@registration_page.route("/", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        if request.form.get("name"):
            if request.form.get("name") not in users:
                print('user is ok')

                if request.form.get("email"):
                    print('email is ok')
                    if request.form.get("phone_number"):
                        if request.form.get("password"):
                            print(12)
                            users[request.form.get("name")] = [request.form.get("password"), request.form.get("email"),
                                                               request.form.get("phone_number")]
                            print(users)

                        else:
                            print('enter password')
                            error = 'enter password'
                            return render_template('registration.html', error=error)
                    else:
                        print('enter phone number')
                        error = 'enter phone number'
                        return render_template('registration.html', error=error)

                else:
                    print('enter email')
                    error = 'enter email'
                    return render_template('registration.html', error=error)

        else:
            print('enter username')
            error = 'enter username'
            return render_template('registration.html', error=error)

        return redirect(url_for('login.hello'))
    return render_template("registration.html", error=False)