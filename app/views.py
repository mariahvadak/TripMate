from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from .models import ToDoList, Task
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html')

@views.route('/to-do-lists/', methods=['GET', 'POST'])
def to_do_lists():
    if request.method == 'POST':
        # Get the title of the new to-do list from the form
        title = request.form.get('title')
        # Create a new to-do list object
        new_list = ToDoList(title=title, user=current_user)
        # Add the to-do list to the database
        db.session.add(new_list)
        db.session.commit()
        return redirect(url_for('views.to_do_lists'))

    # If the user is trying to edit a to-do list, get the ID of the list and render the to-do list template
    list_id = request.args.get('list_id')
    if list_id:
        to_do_list = ToDoList.query.filter_by(id=list_id, user=current_user).first()
        if to_do_list:
            # If the list exists, get all its tasks and render the to-do list template
            tasks = Task.query.filter_by(to_do_list_id=list_id).all()
            return render_template('to-do-list.html', to_do_list=to_do_list, tasks=tasks)

    # If the user is not trying to edit a to-do list, render the dashboard template with all the to-do lists
    to_do_lists = ToDoList.query.filter_by(user=current_user).all()
    return render_template('to-do-list.html', to_do_lists=to_do_lists)

@views.route('/todo-doc/')
def doc():
    return render_template('todo_doc.html')