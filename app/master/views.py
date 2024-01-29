from datetime import datetime
import platform
from flask import request, render_template

from app.master import master_bp


def get_data():
    operating_system = platform.system()
    user_agent = request.headers.get('User-Agent')
    time_now = datetime.now()
    return {
        "operating_system": operating_system,
        "user_agent": user_agent,
        "time_now": time_now,
    }


@master_bp.route('/')
def home():
    return render_template('page1.html', data=get_data())


@master_bp.route('/page2')
def page2():
    return render_template('page2.html', data=get_data())


@master_bp.route('/page3')
def page3():
    return render_template('page3.html', data=get_data())


@master_bp.route("/page4", methods=["GET"])
def page4():
    skills = ["Photo takin", "Music playin", "c++ manual testin"]
    skill = request.args.get("skill", None)

    return render_template("page4.html", data=get_data(), skills=skills, skill=skill, skills_len=len(skills))



