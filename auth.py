from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/signup')
async def signup():
    return render_template('signup.html')

@auth_blueprint.route('/signup', methods=['POST'])
async def signup_post():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    email_check = User.query.filter_by(email=email).first()
    if user:
        flash('User with this username already exists', category='error')
        return redirect(url_for('auth.signup'))
    if email_check:
        flash('This email already exists, pick another please', category='error')
        return redirect(url_for('auth.signup'))
    
    new_user = User(username=username, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
    try:
        db.session.add(new_user)
        db.session.commit()
        flash('Successfully done signuping ^)', category='success')
        return redirect(url_for('auth.login'))
    except Exception as e:
        print(e)
        flash('Something went wrong with database, please try again...', category='error')
        return redirect(url_for('auth.signup'))

@auth_blueprint.route('/login')
async def login():
    return render_template('login.html')

@auth_blueprint.route('/login', methods=['POST'])
async def login_post():
    email = request.form['email']
    password = request.form['password']
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    if not user:
        flash('This user is not exists, please login with correct parameters', category='error')
        return redirect(url_for('auth.login'))

    if not check_password_hash(user.password, password):
        flash('Incorrect password', category='error')
        return redirect(url_for('auth.login'))
    
    login_user(user, remember=remember)
    flash('Successfully logged in', category='success')
    return redirect(url_for('main.main_page'))

@auth_blueprint.route('/logout')
async def logout():
    logout_user()
    flash('Successfully logged out', category='success')
    return redirect(url_for('main.main_page'))