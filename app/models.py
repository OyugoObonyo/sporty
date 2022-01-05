from datetime import datetime
from sqlalchemy.orm import backref
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    A class reprsenting a user table in the database
    """
    id = db.Column(db.Integer, index=True, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    products = db.relationship('Product', backref='vendor', lazy='dynamic')

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


class Product(db.Model):
    """
    A class representing a product table in the database
    """
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    vendor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


class Brand(db.Model):
    """
    A class representing a brand table in the database
    """
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(40))
    products = db.relationship('Product', backref='brand', lazy='dynamic')


class Category(db.Model):
    """
    A class representing a Category table in the database
    """
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(40))
    products = db.relationship('Product', backref='category', lazy='dynamic')
