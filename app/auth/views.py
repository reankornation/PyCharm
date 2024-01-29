import platform

from datetime import datetime

from app import db
from app.auth import authet_bp
from app.auth.forms import LoginForm, RegistrationForm, ChangePassword


def get_data():
    operating_system = platform.system()
    user_agent = request.headers.get('User-Agent')
    time_now = datetime.now()
    return {
        "operating_system": operating_system,
        "user_agent": user_agent,
        "time_now": time_now,
    }


from flask import redirect, url_for, flash, render_template, request
from flask_login import current_user, login_user, login_required, logout_user

from app.models import User


@authet_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.account'))
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter(User.email == email).first()

        if user is None or not user.verify_password(password):
            flash("invalid email or password!", "danger")
            return redirect(url_for("authet.login"))

        flash("Login succesfull!", "success")
        if remember:
            login_user(user, remember=True)
            return redirect(url_for("user.account"))
        return redirect(url_for("authet.login"))

    return render_template("login.html", data=get_data(), form=form)


@authet_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('cookie.info'))
    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = User()
        user.email = email
        user.username = username
        user.password = password

        db.session.add(user)
        db.session.commit()
        flash("Register succesfull!", "success")
        return redirect(url_for("authet.login"))

    return render_template("register.html", data=get_data(), form=form)


@authet_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('authet.login'))


@authet_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        # user = User.query.get(current_user.id)
        if not current_user.verify_password(form.old_password.data):
            flash("Old password is incorect", "danger")
            return redirect(url_for('user.account'))
    current_user.password = form.new_password.data
    db.session.commit()
    flash("Password changed!", "success")
    return redirect(url_for('user.account'))
