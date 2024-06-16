from flask import flash, redirect, render_template, request, url_for, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from app.blueprints import main
from app.forms import *
from app.models import *

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('main.login'))
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, score = 0)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('signUp.html', form=form)

@main.route('/score', methods=['POST'])
@login_required
def score():
    current_user.score += 1
    db.session.commit()
    return jsonify({'score': current_user.score})

@main.route('/top_users', methods=['GET'])
def top_users():
    top_users = db.session.query(User).order_by(User.score.desc()).limit(10).all()
    users_list = [{'username': user.username, 'score': user.score} for user in top_users]
    return jsonify({'top_users': users_list})