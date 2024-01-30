import os
from datetime import datetime

from flask import render_template, request, redirect, url_for
from flask import session, make_response
from flask_login import login_required, current_user, logout_user, login_user
from flask import current_app as app
from werkzeug.utils import secure_filename
import platform
from app import db
from .forms import LoginForm, RegistrationForm, ChangePassword, UpdateAccountForm
from .forms import TodoForm
from .models import Todo, User


def get_data():
    operating_system = platform.system()
    user_agent = request.headers.get('User-Agent')
    time_now = datetime.now()
    return {
        "operating_system": operating_system,
        "user_agent": user_agent,
        "time_now": time_now,
    }


@app.route('/')
def home():
    return render_template('page1.html', data=get_data())


@app.route('/page2')
def page2():
    return render_template('page2.html', data=get_data())


@app.route('/page3')
def page3():
    return render_template('page3.html', data=get_data())


@app.route("/page4", methods=["GET"])
def page4():
    skills = ["Photo takin", "Music playin", "c++ manual testin"]
    skill = request.args.get("skill", None)

    return render_template("page4.html", data=get_data(), skills=skills, skill=skill, skills_len=len(skills))


from flask import flash


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter(User.email == email).first()

        if user is None or not user.verify_password(password):
            flash("invalid email or password!", "danger")
            return redirect(url_for("login"))

        flash("Login succesfull!", "success")
        if remember:
            login_user(user, remember=True)
            return redirect(url_for("account"))
        return redirect(url_for("login"))

    return render_template("login.html", data=get_data(), form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('info'))
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
        return redirect(url_for("login"))

    return render_template("register.html", data=get_data(), form=form)


@app.route('/info', methods=['GET'])
@login_required
def info():
    cookies = request.cookies
    return render_template('info.html', data=get_data(), cookies=cookies)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/add_cookie', methods=["GET", "POST"])
@login_required
def add_cookie():
    if 'username' in session:
        key = request.form['key']
        value = request.form['value']

        response = make_response(redirect(url_for('info')))
        response.set_cookie(key, value)
        return response
    else:
        return redirect(url_for('login'))


@app.route('/delete_all_cookies', methods=['GET'])
@login_required
def delete_all_cookies():
    if 'username' in session:
        response = make_response(redirect(url_for('info')))
        for key in request.cookies.keys():
            response.delete_cookie(key)
        return response
    else:
        return redirect(url_for('login'))


@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        # user = User.query.get(current_user.id)
        if not current_user.verify_password(form.old_password.data):
            flash("Old password is incorect", "danger")
            return redirect(url_for('account'))
    current_user.password = form.new_password.data
    db.session.commit()
    flash("Password changed!", "success")
    return redirect(url_for('account'))


@app.route('/todo', methods=['GET', 'POST'])
def todo():
    form = TodoForm()

    if form.validate_on_submit():
        new_todo = Todo(title=form.title.data, description=form.description.data)
        db.session.add(new_todo)
        db.session.commit()
        flash('Todo added successfully!', 'success')
        return redirect(url_for('todo'))

    todos = Todo.query.all()
    return render_template('todo.html', data=get_data(), form=form, todos=todos)


@app.route('/todo/<int:todo_id>', methods=['GET', 'POST'])
def edit_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    form = TodoForm(obj=todo)

    if form.validate_on_submit():
        todo.title = form.title.data
        todo.description = form.description.data
        todo.status = form.status.data
        db.session.commit()
        flash('Todo updated successfully!', 'success')
        return redirect(url_for('todo'))

    return render_template('edit_todo.html', data=get_data(), form=form, todo=todo)


@app.route('/todo/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted successfully!', 'success')
    return redirect(url_for('todo'))


@app.route("/users")
@login_required
def users():
    all_users = User.query.all()
    return render_template('users.html', all_users=all_users, data=get_data())


@app.route("/account")
@login_required
def account():
    form = ChangePassword()
    update_form = UpdateAccountForm()
    update_form.new_email.data = current_user.email
    update_form.new_username.data = current_user.username
    update_form.about_me.data = current_user.about_me
    return render_template('account.html', title='Account', data=get_data(), form=form, update_form=update_form)


@app.route('/change_login', methods=['POST'])
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
    return redirect(url_for('account'))


@app.after_request
def update_user_last_seen(resp):
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()
        
    return resp
