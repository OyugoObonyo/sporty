from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import backref
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """
    A class reprsenting a user table in the database
    """
    id = db.Column(db.Integer, index=True, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    user_uuid = db.Column(db.String(36))
    password_hash = db.Column(db.String(128))
    products = db.relationship('Product', backref='vendor', lazy='dynamic')
    cart = db.relationship('Cart', backref='owner', uselist=False)

    def set_password(self, password):
        """
        Method that generates users' password hashes
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Method that confirms password hashes are indeed from users' passwords
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "User: {}".format(self.username)


@login.user_loader
def load_user(id):
    """
    A user loader function that aids flask in geting user id
    so as to store it in session
    """
    return User.query.get(int(id))


class Product(db.Model):
    """
    A class representing a product table in the database
    """
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    prod_uuid = db.Column(db.String(36))
    image_file = db.Column(db.String(40))
    price = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    vendor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))

    def __repr__(self):
        return "Product: {}".format(self.name)


class Brand(db.Model):
    """
    A class representing a brand table in the database
    """
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(40))
    products = db.relationship('Product', backref='brand', lazy='dynamic')

    def __repr__(self):
        return "Brand: {}".format(self.name)


class Category(db.Model):
    """
    A class representing a Category table in the database
    """
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(40))
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def __repr__(self):
        return "Category: {}".format(self.name)


class Cart(db.Model):
    """
    A class representing a cart table in the database
    """
    id = db.Column(db.Integer, index=True, primary_key=True)
    count = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    products = db.relationship('Product', backref='cart', lazy='dynamic')

    def add_count(self):
        """
        Method which adds cart count by one if product is added to cart
        """
        self.count = self.count + 1

    def __repr__(self):
        return "Cart_ID: {}".format(self.id)
