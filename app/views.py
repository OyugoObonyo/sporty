from os import name
from werkzeug.utils import redirect
from wtforms.fields.simple import EmailField
from app import app, db
from flask import render_template, flash, url_for
from app.forms import LoginForm, RegistrationForm, ProductForm
from app.models import Product, User, Category, Brand
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import secure_filename
import os
import uuid


@app.route('/')
@app.route('/index', strict_slashes=False)
def index():
    products = Product.query.all()
    return render_template('/index.html', title='Home', products=products)


@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    """
    A route that handles user registration
    """
    # Handles the odd scenario where a registered user visits the /register view
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations! Registration was successful')
        return redirect(url_for('login'))
    return render_template('/register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """
    Route which handles user log ins
    """
    # Handles odd scenario where logged in user tries to access /login view
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid Username or Password")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Log In', form=form)


@app.route('/logout', methods=['GET', 'POST'], strict_slashes=False)
def logout():
    """
    View to handle user logouts
    """
    logout_user()
    return redirect(url_for('index'))


def save_image(image_file):
    """
    Function that saves an image in the program
    """
    image = image_file.filename
    image_path = os.path.join(app.root_path())



@app.route('/create', methods=['GET', 'POST'])
def create():
    """
    View that creates a product in the database
    """
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, description=form.description.data, brand_id=form.brand.data, category_id=form.category.data, price=form.price.data, vendor=current_user)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html', title='Create', form=form)
