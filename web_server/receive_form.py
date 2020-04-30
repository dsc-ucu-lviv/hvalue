from flask import Blueprint, render_template, request, redirect, url_for
import database.db

receive_form_page = Blueprint('receive-form', __name__, template_folder='templates')


cities = {'Lviv': 0}
rcv_station_types = {'container': 0, 'organisation': 1}
category_types = {'Money': 0, 'Clothes': 1, 'Food': 2}


@receive_form_page.route("/receive-form", methods=["GET", "POST"])
def get_data():
    if database.db.profile_info is None:
        return redirect(url_for('login.login'))
    if request.method == "POST":
        if request.form.get("address"):
            if request.form.get("city") and request.form.get("time_to")\
                    and request.form.get("time_out") and request.form.get("description"):
                input_data = {'user_id': database.db.profile_info['user_id'],
                              'type_id': request.form.get('type-org'),
                              'categories': request.form.getlist("categories"),
                              'locations': [request.form.get('city'), request.form.get('address')],
                              'time_from': request.form.get('time_to'),
                              'time_to': request.form.get('time_out'),
                              'description': request.form.get('description')}
                print(input_data)
                database.db.db.db_station.add_easy_rcv_station(
                    {'user_id': database.db.profile_info['user_id'],
                     'type_id': rcv_station_types[request.form.get('type-org')],
                     'categories': [category_types[type] for type in request.form.getlist("categories")],
                     'address': request.form.get('address'),
                     'time_from': request.form.get('time_to'),
                     'name': request.form.get('name'),
                     'time_to': request.form.get('time_out'),
                     'description': request.form.get('description')})
                return redirect(url_for('profile_org.profile_org'))
            else:
                error = 'enter all information'
                return render_template('add_receive_station.html', error=error, profile_info=database.db.profile_info)
        else:
            error = 'enter all information'
            return render_template('add_receive_station.html', error=error, profile_info=database.db.profile_info)

    return render_template("add_receive_station.html", profile_info=database.db.profile_info)
