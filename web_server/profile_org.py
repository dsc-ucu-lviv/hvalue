from flask import Blueprint, render_template, request, redirect, url_for
import database.db


profile_org_page = Blueprint('profile_org', __name__, template_folder='templates')


def _redirect_url(default='login.login'):
    """
    Helper f-n for redirecting back from unauthorized roots.
    :param default: base root (e.g. app's main page)
    :return: url for back-redirection
    """
    return request.args.get('next') or request.referrer or url_for(default)


@profile_org_page.route("/profile_org", methods=["GET", "POST"])
def profile_org():
    if request.method == "POST":
        return "?"
    if database.db.profile_info is not None:
        org_stations = database.db.db.db_station.get_profile_info(database.db.profile_info["user_id"])['stations'] or []
        org_profile = {'org_name': database.db.profile_info['username'],
                       'org_type': database.db.profile_info['type_id'],
                       'email': database.db.profile_info.get('email'),
                       'phone_number': database.db.profile_info.get('phone_number'),
                       'num_stations': len(org_stations) if org_stations else 0}

        return render_template("profile_org.html", org=org_profile, stations=org_stations,
                               profile_info=database.db.profile_info)

    return redirect(_redirect_url())