from app import db
from app.main import bp
from flask import render_template
from flask_login import current_user
from app.models import User, Product
from flask_login import login_required

BRANDS = ['Nike', 'Adidas', 'Puma', 'New Balance', 'Kalenji', 'Others']
CATEGORIES = ['Shoes', 'Jerseys', 'Tracksuits', 'Sneakers', 'Others']


@bp.route('/')
@bp.route('/index', strict_slashes=False)
def index():
    brands = BRANDS
    categories = CATEGORIES
    products = Product.query.filter(Product.vendor_id != current_user.id).all()
    return render_template('main/index.html', title='Home', products=products, brands=brands, categories=categories)


@bp.route('/profile/<id>')
@login_required
def get_profile(id):
    """
    Renders profile page of particular user
    """
    brands = BRANDS
    categories = CATEGORIES
    user = User.query.get(id)
    name = user.username
    id = user.id
    products = Product.query.filter_by(vendor_id=id).all()
    return render_template('main/profile.html', title=name, products=products, brands=brands, categories=categories)
