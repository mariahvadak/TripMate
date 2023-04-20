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
        if user == current_user:
            flash("You're already logged in", category='login-error')
            return redirect(url_for('views.home_page', user=user))
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home_page', user=user))
            else:
                flash('Incorrect password, please try again', category='login-error')
        else:
            flash('Email does not exist', category='login-error')
            
    return render_template("login.html", user=current_user)

@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.landing_page'))

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
            flash('Email already exists.', category='signup-error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='signup-error')
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


@auth.route('/updatepw/', methods=['GET', 'POST'])
def update_pw():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        password1 = request.form.get('password1')
        print(password1)
        password2 = request.form.get('password2')
        if user:
            if password1 != password2:
                flash('Passwords don\'t match.', category='pw-error')
                return render_template("updatepw.html")
            else:    
                password=generate_password_hash( request.form.get('password1'), method='sha256')
                user.password = password
                db.session.commit()
                flash('Update password succesfully', category='pw-success')
                return render_template("updatepw.html")
        else:
            flash('Email does not exist', category='pw-error')
    return render_template("updatepw.html")