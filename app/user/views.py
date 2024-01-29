import os
from datetime import datetime

from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app import db
from app.auth.forms import ChangePassword
from app.models import User
from app.user import user_bp
from app.user.forms import UpdateAccountForm


def get_data():
    operating_system = os.uname()
    user_agent = request.headers.get('User-Agent')
    time_now = datetime.now()
    return {
        "operating_system": operating_system,
        "user_agent": user_agent,
        "time_now": time_now,
    }


@user_bp.route("/users")
@login_required
def users():
    all_users = User.query.all()
    return render_template('users.html', all_users=all_users, data=get_data())


@user_bp.route("/account")
@login_required
def account():
    form = ChangePassword()
    update_form = UpdateAccountForm()
    update_form.new_email.data = current_user.email
    update_form.new_username.data = current_user.username
    update_form.about_me.data = current_user.about_me
    return render_template('account.html', title='Account', data=get_data(), form=form, update_form=update_form)


@user_bp.route('/change_login', methods=['POST'])
@login_required
def change_login():
    form = UpdateAccountForm()
    if not form.validate_on_submit():
        # if not current_user.verify_password(form.old_password.data):
        #     flash("Old password is incorect", "danger")
        return render_template('account.html', title='Account', data=get_data(), form=ChangePassword(),
                               update_form=form)
        # return redirect(url_for('account'))
    current_user.username = form.new_username.data
    current_user.email = form.new_email.data
    current_user.about_me = form.about_me.data
    profile_photo = form.profile_picture.data
    if profile_photo:
        filename = secure_filename(profile_photo.filename)
        filepath = os.path.join('app/static/images/', filename)
        profile_photo.save(filepath)
        current_user.image_file = filename

    db.session.commit()
    flash("Your data was changed!", "success")
    return redirect(url_for('user.account'))


@user_bp.after_request
def update_user_last_seen(resp):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()

    return resp
