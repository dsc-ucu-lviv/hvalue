from flask import Flask, redirect, url_for

from web_server.login import login_page
from web_server.registration import registration_page
from web_server.receive_form import receive_form_page
from web_server.map import map_page



app = Flask(__name__)
app.register_blueprint(registration_page)
app.register_blueprint(login_page)
app.register_blueprint(receive_form_page)
app.register_blueprint(map_page)


@app.route("/")
def render_main_page():
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
