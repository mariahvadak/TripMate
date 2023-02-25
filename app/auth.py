from flask import Blueprint,render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        print(user)
        print(password)
        print(user.password)
        if user:
            if check_password_hash(user.password, password):
                flash('Log in succesfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home_page'))
            else:
                flash('Incorrect password, please try again', category='error')
        else:
            flash('Email does not exist', category='error')
            
    return render_template("login.html", user=current_user)

@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            #Create a new row in the db
            new_user = User(email=email, first_name=firstName, last_name=lastName, password=generate_password_hash(password1, method='sha256'))
            #Add a new row to the db
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Your account has been created succesfully!', category='success')
            return redirect(url_for('views.home_page'))
           
    return render_template('signup.html')
