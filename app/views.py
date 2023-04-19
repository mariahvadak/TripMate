from flask import Blueprint, render_template, request, redirect, url_for
from flask import jsonify
from flask_login import current_user, login_required
from .models import TodoList
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html')

@views.route('/todolists/', methods=['GET', 'POST'])
@login_required
def todolist():
    # Query all the to-do lists from the database
    to_do_lists = TodoList.query.all()

    if request.method == 'POST':
        # Get the title of the new to-do list from the form data
        title = request.json.get('title')

        # Create a new to-do list object and add it to the database
        new_todo_list = TodoList(title=title, user_id=current_user.id)
        db.session.add(new_todo_list)
        db.session.commit()

        # Return the ID of the newly created todo list as a JSON response
        return jsonify(id=new_todo_list.id)

    # Render the to-do list template with the list of to-do lists and links to each individual to-do list
    return render_template('to-do-list.html', to_do_lists=to_do_lists, individual_links=True)

@views.route('/todolists/<int:todo_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_todo_list(todo_id):
    # Query the todo list with the specified ID from the database
    todo_list = TodoList.query.get(todo_id)

    if request.method == 'POST':
        # Update the title of the todo list
        todo_list.title = request.form['title']
        db.session.commit()

        # Redirect the user to the todo list dashboard
        return redirect(url_for('views.todolist'))

    # Render the edit todo list template with the specified todo list and its items
    return render_template('todo_doc.html', todo_list=todo_list)

@views.route('/todo-doc/')
def doc():
    return render_template('todo_doc.html')