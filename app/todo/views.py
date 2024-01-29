import platform
from datetime import datetime

from flask import current_app as app
from flask import flash
from flask import render_template, request, redirect, url_for

from app import db
from app.models import Todo
from app.todo import todo_bp
from app.todo.forms import TodoForm


def get_data():
    operating_system = platform.system()
    user_agent = request.headers.get('User-Agent')
    time_now = datetime.now()
    return {
        "operating_system": operating_system,
        "user_agent": user_agent,
        "time_now": time_now,
    }



@todo_bp.route('/todo', methods=['GET', 'POST'])
def todo():
    form = TodoForm()

    if form.validate_on_submit():
        new_todo = Todo(title=form.title.data, description=form.description.data)
        db.session.add(new_todo)
        db.session.commit()
        flash('Todo added successfully!', 'success')
        return redirect(url_for('todo.todo'))

    todos = Todo.query.all()
    return render_template('todo.html', data=get_data(), form=form, todos=todos)


@todo_bp.route('/todo/<int:todo_id>', methods=['GET', 'POST'])
def edit_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    form = TodoForm(obj=todo)

    if form.validate_on_submit():
        todo.title = form.title.data
        todo.description = form.description.data
        todo.status = form.status.data
        db.session.commit()
        flash('Todo updated successfully!', 'success')
        return redirect(url_for('todo.todo'))

    return render_template('edit_todo.html', data=get_data(), form=form, todo=todo)


@todo_bp.route('/todo/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted successfully!', 'success')
    return redirect(url_for('todo.todo'))

