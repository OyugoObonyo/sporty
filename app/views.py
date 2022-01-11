from itertools import product
from os import name
from werkzeug.utils import redirect
from app import app, db
from flask import render_template, flash, url_for, session, request
from app.forms import LoginForm, RegistrationForm, ProductForm
from app.models import Product, User, Category, Brand
from flask_login import current_user, login_user, logout_user
from werkzeug.exceptions import RequestEntityTooLarge
import os
import uuid
from PIL import Image


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
    Function that saves image passed as an arg to it
    and return the image's filename
    """
    image_id = str(uuid.uuid4())
    file = image_id + '.png'
    file_path = os.path.join(app.root_path, app.config['PRODUCT_IMAGES_DIR'], file)
    # Utilize PIL library to manipulate image_file
    Image.open(image_file).save(file_path)
    return file


@app.route('/create', methods=['GET', 'POST'])
def create():
    """
    View that creates a product in the database
    """
    # Catch error resulting from user publishing an image > 16MB
    try:
        form = ProductForm()
        if form.validate_on_submit():
            f = form.image.data
            img_file = save_image(f)
            product_uuid = str(uuid.uuid4())
            product = Product(name=form.name.data, description=form.description.data, brand_id=form.brand.data, image_file=img_file, category_id=form.category.data, price=form.price.data, prod_uuid=product_uuid, vendor=current_user)
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('index'))
    except RequestEntityTooLarge:
        return "Upload Limit is 16 MB"
    return render_template('create.html', title='Create', form=form)


def merge_dict(dict_1, dict_2):
    """
    Function that merges items from two dictionaries
    into a single dict
    """
    if isinstance(dict_1, list) and isinstance(dict_2, list):
        return dict_1 + dict_2
    else:
        return dict(list(dict_1.items()) + list(dict_2.items()))


@app.route('/add-to-cart', methods=['GET', 'POST'])
def add_to_cart():
    """
    Route that is triggered when user adds item to cart
    """
    prod_id = request.form.get('product_id')
    product = Product.query.filter_by(id=prod_id).first()
    dic_items = {prod_id: {'name': product.name, 'description': product.description, 'price': product.price}}
    if 'cart' in session:
        if prod_id in session['cart']:
            flash('This item is already in your cart')
            return redirect(request.referrer)
        else:
            session['cart'] = merge_dict(session['cart'], dic_items)
            return redirect(request.referrer)
    else:
        session['cart'] = dic_items
        return redirect(request.referrer)


@app.route('/display-cart')
def display_cart():
    """
    Route that displays a user's cart
    """
    if 'cart' not in session:
        flash("Your cart is currently empty")
        return redirect(request.referrer)
    total_price = 0
    for key, product in session['cart'].items():
        total_price += product['price']
    return render_template('/cart.html', title='Cart', total_price=total_price)


@app.route('/delete-from-cart/<uuid>')
def delete_from_cart():
    """
    View triggered when user want to delete item from cart
    """
    product = Product.query.filter_by
    pass


@app.route('/buy/<int:id>', methods=['GET', 'POST'])
def buy(id):
    """
    View that handles user purchases
    """
    pass
    