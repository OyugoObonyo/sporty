import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    A class that stores the apps configuration variables
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Modify db env name to cofer with sqlalchemy's new dialect
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1) or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRODUCT_IMAGES_DIR = "static/images/products"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
