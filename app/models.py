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

    def __repr__(self):
        return (self.username)


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
    image_file = db.Column(db.String(40))
    price = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    vendor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    brand = db.Column(db.String(12))
    category = db.Column(db.String(12))

    def __repr__(self):
        return "Product: {}".format(self.name)
