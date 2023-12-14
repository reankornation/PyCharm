# app.py

import os
import datetime
from flask import Flask, render_template, request
import random

app = Flask(__name__)

my_skills = [
    "Знання англійської мови",
    "Економічні навички",
    "Програмування на Python",
    "Веб-розробка з використанням Flask",
    "Аналіз даних та візуалізація",
]

project_info = {
    "project_title": "Flask",
    "project_description": "Ціль проекту навичитись працювати з Flask.",
    "project_tech_stack": ["Python", "Flask", "HTML", "CSS", "JavaScript"],
    "project_links": {
        "GitHub": "https://github.com/reankornation",
    },
}

# Функція для генерації випадкової інформації для портфоліо
def generate_random_portfolio_info():
    projects = []
    for i in range(1):  # Додати стільки проектів, скільки потрібно
        project = {
            "title": f"Технології",
            "description": f"Інтересні факти про штучний інтелект та машинне навчання.. {random.choice(['Огляд останніх технологічних досягнень у сфері робототехніки.'])}",
            "tools": random.sample(my_skills, k=random.randint(1, len(my_skills))),
        }
        projects.append(project)
    return projects

@app.route('/')
def index():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    return render_template('index.html', data=data)

@app.route('/about')
def about():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    return render_template('about.html', data=data, project_info=project_info)

@app.route('/portfolio')
def portfolio():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    portfolio_info = generate_random_portfolio_info()  # Отримання випадкової інформації
    return render_template('portfolio.html', data=data, portfolio_info=portfolio_info)

@app.route('/skills', defaults={'id': None})
@app.route('/skills/<int:id>')
def skills(id):
    data = [os.name, datetime.datetime.now(), request.user_agent]
    return render_template('skills.html', id=id, skills=my_skills, data=data)

if __name__ == '__main__':
    app.run(debug=True)
