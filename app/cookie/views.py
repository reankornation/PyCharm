from datetime import datetime
import platform


from flask import request, render_template, session, make_response, redirect, url_for
from flask_login import login_required

from app.cookie import cookie_bp


def get_data():
    operating_system = platform.system()
    user_agent = request.headers.get('User-Agent')
    time_now = datetime.now()
    return {
        "operating_system": operating_system,
        "user_agent": user_agent,
        "time_now": time_now,
    }


@cookie_bp.route('/info', methods=['GET'])
@login_required
def info():
    cookies = request.cookies
    return render_template('info.html', data=get_data(), cookies=cookies)


@cookie_bp.route('/add_cookie', methods=["GET", "POST"])
@login_required
def add_cookie():
    if 'username' in session:
        key = request.form['key']
        value = request.form['value']

        response = make_response(redirect(url_for('cookie.info')))
        response.set_cookie(key, value)
        return response
    else:
        return redirect(url_for('authet.login'))


@cookie_bp.route('/delete_all_cookies', methods=['GET'])
@login_required
def delete_all_cookies():
    if 'username' in session:
        response = make_response(redirect(url_for('cookie.info')))
        for key in request.cookies.keys():
            response.delete_cookie(key)
        return response
    else:
        return redirect(url_for('authet.login'))
