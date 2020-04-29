from flask import Blueprint, render_template, request, redirect, url_for

receive_form_page = Blueprint('receive-form', __name__, template_folder='templates')


@receive_form_page.route("/receive-form", methods=["GET", "POST"])
def get_data():
    if request.method == "POST":
        if request.form.get("address"):
            if request.form.get("city") and request.form.get("time_to")\
                    and request.form.get("time_out") and request.form.get("description"):
                input_data = {'user_id': 123456,
                              'type_id': 123456,
                              'categories': request.form.getlist("categories"),
                              'locations': [request.form.get('city'), request.form.get('address')],
                              'time_from': request.form.get('time_to'),
                              'time_to': request.form.get('time_out'),
                              'description': request.form.get('description')}
                # print(input_data)
                # return input_data
            else:
                error = 'enter all information'
                return render_template('add_receive_station.html', error=error)
        else:
            error = 'enter all information'
            return render_template('add_receive_station.html', error=error)

    return render_template("login.html")
