from flask import Blueprint, render_template

views = Blueprint('views',__name__)

@views.route('/')
def home_page():
    return render_template("home.html")

@views.route('/to-do-lists/')
def to_do_lists():
    # Fetch the list of to-do lists from a database or file system
    to_do_lists = ['To-Do List 1', 'To-Do List 2', 'To-Do List 3', 'To-Do List 4', 'To-Do List 5', 'To-Do List 6', 
                   'To-Do List 7','To-Do List 8', 'To-Do List 9', 'To-Do List 10',]

    # Pass the list of to-do lists to the to-do list template
    return render_template("to-do-list.html", to_do_lists=to_do_lists)

@views.route('/todo-doc/')
def to_do_doc():
    
    return render_template("todo_doc.html")