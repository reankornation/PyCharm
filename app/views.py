from app import app
from flask import request, render_template, session, redirect, url_for, make_response
import platform
from os.path import dirname, realpath, join
from datetime import datetime
from flask import current_app
import json

app.secret_key = b"abmobusd"


@app.route('/')
def home():
    operating_system = platform.system()
    user_agent = request.headers.get('User-Agent')
    time_now = datetime.now()
    data = {
        "operating_system": operating_system,
        "user_agent": user_agent,
        "time_now": time_now,
    }
    return render_template('page1.html', data=data)


@app.route('/page2')
def page2():
    operating_system = platform.system()
    user_agent = request.headers.get('User-Agent')
    time_now = datetime.now()
    data = {
        "operating_system": operating_system,
        "user_agent": user_agent,
        "time_now": time_now,
    }
    return render_template('page2.html', data=data)


@app.route('/page3')
def page3():
    operating_system = platform.system()
    user_agent = request.headers.get('User-Agent')
    time_now = datetime.now()
    data = {
        "operating_system": operating_system,
        "user_agent": user_agent,
        "time_now": time_now,
    }
    return render_template('page3.html', data=data)


@app.route("/page4", methods=["GET"])
def page4():
    operating_system = platform.system()
    user_agent = request.headers.get('User-Agent')
    time_now = datetime.now()
    data = {
        "operating_system": operating_system,
        "user_agent": user_agent,
        "time_now": time_now,
    }
    skills = ["Photo takin", "Music playin", "c++ manual testin"]
    skill = request.args.get("skill", None)

    return render_template("page4.html", data=data, skills=skills, skill=skill, skills_len=len(skills))


@app.route('/login', methods=["GET", "POST"])
def login():
    operating_system = platform.system()
    user_agent = request.headers.get('User-Agent')
    time_now = datetime.now()
    data = {
        "operating_system": operating_system,
        "user_agent": user_agent,
        "time_now": time_now,
    }

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        dataJsonPath = join(dirname(realpath(__file__)), 'auth_data.json')
        with open(dataJsonPath, 'r', encoding='utf-8') as file:
            auth_data = json.load(file)

        if username in auth_data and auth_data[username] == password:
            session['username'] = username
            return redirect(url_for('info'))

    return render_template("login.html", data=data)


@app.route('/info', methods=['GET'])
def info():
    operating_system = platform.system()
    user_agent = request.headers.get('User-Agent')
    time_now = datetime.now()
    data = {
        "operating_system": operating_system,
        "user_agent": user_agent,
        "time_now": time_now,
    }

    username = session.get('username', None)

    if username:
        cookies = request.cookies

        return render_template('info.html', username=username, data=data, cookies=cookies)
    else:
        return redirect(url_for('login'))

@app.route('/logout', methods=['GET'])
def logout():
    operating_system = platform.system()
    user_agent = request.headers.get('User-Agent')
    time_now = datetime.now()
    data = {
        "operating_system": operating_system,
        "user_agent": user_agent,
        "time_now": time_now,
    }

    username = session.get('username', None)

    if username:
        session.pop(username, None)
        return render_template('login.html', username=username, data=data)
    else:
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
        dataJsonPath = platform.path.join(current_app.root_path, 'auth_data.json')

        with open(dataJsonPath, 'r', encoding='utf-8') as file:
            auth_data = json.load(file)

        if username in auth_data:
            auth_data[username] = new_password

            with open(dataJsonPath, 'w', encoding='utf-8') as file:
                json.dump(auth_data, file, ensure_ascii=False, indent=4)

        return redirect(url_for('info'))
    else:
        return redirect(url_for('login'))
