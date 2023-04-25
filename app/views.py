from flask import Blueprint, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from flask import Flask, render_template, request, redirect, url_for
from app import models
from app.models import User, Todolist, Task
from datetime import date, datetime
from . import db  
import datetime

views = Blueprint('views',__name__)

@views.route('/')
def landing_page():
    return render_template("landing.html")

@views.route('/home', methods=['GET'])
@login_required
def home_page():
    return render_template("home.html", user=current_user)

@views.route('/signup/')
def signup_page():
    return render_template("signup.html")

@views.route('/calendar/', methods=['GET', 'POST'])
@login_required
def calendar():
    date = datetime.date.today().strftime("%m-%d-%Y")
    userId = current_user.get_id()
    # todolist = Todolist.query.filter_by(user=userId).all()
    if request.method == 'POST':
        date = request.form.get('selectedDay')
    tasks = Task.query.filter_by(user= userId, date=date, complete = False).all()
    return render_template("calendar.html", date=date, tasks = tasks)
    
@views.route('/todolist/', methods=['GET', 'POST'])
@login_required
def to_do_lists():
    userId = current_user.get_id()
    to_do_lists = Todolist.query.filter_by(user=userId).all()
    if request.method == 'POST':
        title = request.form.get('title')
        created_date = date.today()
        new_list = Todolist(user=userId, date=created_date, title=title )
        db.session.add(new_list)
        db.session.commit()
        return redirect(url_for('views.to_do_lists'))

    return render_template('to-do-list.html', to_do_lists=to_do_lists)

@views.route('/todolist/<title>/', methods=['GET', 'POST'])
@login_required
def doc(title):
    to_do_list = Todolist.query.filter_by(title=title).first()
    tasks = Task.query.filter_by(todolist=to_do_list.id).all()
    if request.method == 'POST':
        userId = current_user.get_id()
        todolist= to_do_list.id
        if request.form.get('datepicker') == '':
            date = datetime.date.today().strftime("%m-%d-%Y")
        else:
            date = datetime.datetime.strptime(request.form.get('datepicker'), "%Y-%m-%d").strftime("%m-%d-%Y")
        print(date)
        text = request.form.get('text')
        complete = False
        new_task = Task(user = userId, todolist=todolist, date=date, text=text, complete=complete)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('views.doc', title=title))
    return render_template('todo_doc.html', to_do_list=to_do_list, tasks=tasks)

@views.route("/update/<title>/<id>/",  methods=['GET','POST'])
def update(title, id):
    task = Task.query.filter_by(id=id).first()
    task.complete = True
    db.session.commit()
    print(task.complete)
    return redirect(url_for("views.doc", title=title))

@views.route("/delete/<int:todo_id>/", methods=['GET', 'POST'])
def delete_list(todo_id):
    todo = Todolist.query.filter_by(id=todo_id).first()
    tasks = Task.query.filter_by(todolist=todo_id).all()
    for task in tasks:
        db.session.delete(tasks)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("views.to_do_lists"))

@views.route("/delete_task/<title>/<int:task_id>/", methods=['GET', 'POST'])
def delete_task(title, task_id):
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("views.doc", title=title))
