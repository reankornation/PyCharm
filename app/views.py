from app import app, db
from flask import session, make_response
import platform
from os.path import dirname, realpath, join
from datetime import datetime
from flask import current_app
from .forms import LoginForm
import json
from flask import render_template, request, redirect, url_for
from .forms import TodoForm
from .models import Todo
from .forms import FeedbackForm
from .models import Feedback


def get_data():
    operating_system = platform.platform()
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
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        dataJsonPath = join(dirname(realpath(__file__)), 'auth_data.json')
        with open(dataJsonPath, 'r', encoding='utf-8') as file:
            auth_data = json.load(file)

        if username in auth_data and auth_data[username] == password:
            if remember:
                session['username'] = username
                return redirect(url_for('info'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    return render_template("login.html", data=get_data(), form=form)


@app.route('/info', methods=['GET'])
def info():
    username = session.get('username', None)

    if username:
        cookies = request.cookies

        return render_template('info.html', username=username, data=get_data(), cookies=cookies)
    else:
        return redirect(url_for('login'))


@app.route('/logout', methods=['GET'])
def logout():
    username = session.get('username', None)
    if username:
        session.pop('username')
    return redirect(url_for('login'))


@app.route('/add_cookie', methods=["GET", "POST"])
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
def delete_all_cookies():
    if 'username' in session:
        response = make_response(redirect(url_for('info')))
        for key in request.cookies.keys():
            response.delete_cookie(key)
        return response
    else:
        return redirect(url_for('login'))


@app.route('/change_password', methods=['POST'])
def change_password():
    if 'username' in session:
        new_password = request.form['new_password']

        username = session['username']
        dataJsonPath = os.path.join(current_app.root_path, 'auth_data.json')

        with open(dataJsonPath, 'r', encoding='utf-8') as file:
            auth_data = json.load(file)

        if username in auth_data:
            auth_data[username] = new_password

            with open(dataJsonPath, 'w', encoding='utf-8') as file:
                json.dump(auth_data, file, ensure_ascii=False, indent=4)

        return redirect(url_for('info'))
    else:
        return redirect(url_for('login'))


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



@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback_entry = Feedback(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(feedback_entry)
        db.session.commit()
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('feedback'))

    feedback_entries = Feedback.query.all()
    operating_system = "Your OS"  # Отримайте ОС з якої відбувається доступ
    return render_template('feedback.html', form=form, feedback_entries=feedback_entries, data={'operating_system': operating_system})