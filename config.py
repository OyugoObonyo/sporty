import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """
    A class that stores the apps configuration variables
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'temporary-hardcoded-string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRODUCT_IMAGES_DIR = "static/images/products"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
