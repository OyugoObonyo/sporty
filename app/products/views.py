from werkzeug.utils import redirect
from app import db
from flask import render_template, flash, url_for, session, request, current_app
from app.products import bp
from app.products.forms import ProductForm
from app.models import Product
from flask_login import current_user, login_required
from werkzeug.exceptions import RequestEntityTooLarge
import os
import uuid
from PIL import Image


BRANDS = ['Nike', 'Adidas', 'Puma', 'New Balance', 'Kalenji', 'Others']
CATEGORIES = ['Shoes', 'Jerseys', 'Tracksuits', 'Sneakers', 'Others']


def save_image(image_file):
    """
    Function that saves image passed as an arg to it
    and return the image's filename
    """
    image_id = str(uuid.uuid4())
    file_name = image_id + '.png'
    file_path = os.path.join(current_app.root_path, current_app.config['PRODUCT_IMAGES_DIR'], file_name)
    # Utilize PIL library to manipulate image_file
    Image.open(image_file).save(file_path)
    return file_name


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """
    View that creates a product in the database
    """
    # Catch error resulting from user publishing an image > 16MB
    brands = BRANDS
    categories = CATEGORIES
    try:
        form = ProductForm()
        if form.validate_on_submit():
            f = form.image.data
            img_file = save_image(f)
            product_uuid = str(uuid.uuid4())
            if form.price.data <= 0:
                flash('Price should be greater than Ksh.0')
                return redirect(url_for('products.create'))
            product = Product(name=form.name.data, brand=form.brand.data, image_file=img_file, category=form.category.data, price=form.price.data, prod_uuid=product_uuid, vendor=current_user)
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('main.index'))
    except RequestEntityTooLarge:
        return "Upload Limit is 16 MB"
    return render_template('products/create.html', title='Create', brands=brands, categories=categories, form=form)


@bp.route('/display-brand/<name>')
def display_brand(name):
    """
    Route which displays all the products of a particular brand
    """
    brands = BRANDS
    categories = CATEGORIES
    products = Product.query.filter_by(brand=name).all()
    return render_template('products/brands.html', title=name, products=products, brands=brands, categories=categories)


@bp.route('/display-category/<name>')
def display_category(name):
    """
    Route which displays all the products of a particular brand
    """
    brands = BRANDS
    categories = CATEGORIES
    products = Product.query.filter_by(category=name).all()
    return render_template('products/categories.html', title=name, products=products, brands=brands, categories=categories)


def merge_dict(dict_1, dict_2):
    """
    Function that merges items from two dictionaries
    into a single dict
    """
    if isinstance(dict_1, list) and isinstance(dict_2, list):
        return dict_1 + dict_2
    else:
        return dict(list(dict_1.items()) + list(dict_2.items()))


@bp.route('/add-to-cart', methods=['GET', 'POST'])
@login_required
def add_to_cart():
    """
    Route that is triggered when user adds item to cart
    """
    prod_id = request.form.get('product_id')
    product = Product.query.filter_by(id=prod_id).first()
    dic_items = {prod_id: {'name': product.name, 'price': product.price, 'vendor': product.vendor_id}}
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


@bp.route('/display-cart')
def display_cart():
    """
    Route that displays a user's cart
    """
    brands = BRANDS
    categories = CATEGORIES
    if 'cart' not in session or len(session['cart']) <= 0:
        flash("Your cart is currently empty")
        return redirect(url_for('main.index'))
    total_price = 0
    for key, product in session['cart'].items():
        total_price += product['price']
    return render_template('products/cart.html', title='Cart', total_price=total_price, brands=brands, categories=categories)


@bp.route('/delete-from-cart/<int:id>')
def delete_from_cart(id):
    """
    View triggered when user want to delete item from cart
    """
    if 'cart' not in session or len(session['cart']) <= 0:
        return redirect(url_for('main.index'))
    session.modified = True
    for key, item in session['cart'].items():
        if int(key) == id:
            session['cart'].pop(key, None)
            return redirect(url_for('products.display_cart'))
    return redirect(url_for('main.index'))


def delete_image(image_file):
    """
    Function that deletes an image file of a particular product
    """
    file_path = file_path = os.path.join(current_app.root_path, current_app.config['PRODUCT_IMAGES_DIR'], image_file)
    os.remove(file_path)


@bp.route('/delete-product', methods=['GET', 'POST'])
def delete_product():
    """
    Function that deletes a product from the database
    """
    prod_id = request.form.get('product_id')
    product = Product.query.filter_by(id=prod_id).first()
    image_file = product.image_file
    db.session.delete(product)
    delete_image(image_file)
    db.session.commit()
    return redirect(request.referrer)
