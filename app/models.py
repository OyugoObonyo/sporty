from app import db
from app.views import index

class User(db.Model):
    """
    A class reprsenting a user in the table in the database
    """
    user_id = db.Column(db.Integer, index=True, primary_key=True)
    username = db.Column()
    email = db.Column()
    password_hash = db.Column()
    products = db.relationship()


class Product(db.Model):
    """
    A class representing a product table in the database
    """
    product_id = db.Column()
    product_name = db.Column()
    product_description = db.Column()
    product_image = db.Column()
    date_posted = db.Column()
    product_vendor = db.Column()
    product_brand = db.Column()
    product_category = db.Column()


class Brand(db.Model):
    """
    A class representing a brand table in the database
    """
    brand_id = db.Column()
    brand_name = db.Column()
    brand_products = db.relationship()


class Category(db.Model):
    """
    A class representing a Category table in the database
    """
    category_id = db.Column()
    brand_name = db.Column()
    category_products = db.relationship()