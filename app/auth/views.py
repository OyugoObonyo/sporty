from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from flask import render_template, flash, url_for, request, redirect
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@bp.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    """
    A route that handles user registration
    """
    # Handles the odd scenario where a registered user visits the /register view
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations! Registration was successful')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """
    Route which handles user log ins
    """
    # Handles odd scenario where logged in user tries to access /login view
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid Username or Password")
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Log In', form=form)


@bp.route('/logout', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def logout():
    """
    View to handle user logouts
    """
    logout_user()
    return redirect(url_for('main.index'))
