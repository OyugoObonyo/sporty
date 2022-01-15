from re import S
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager
from flask_moment import Moment


db = SQLAlchemy()
migrate = Migrate(db, render_as_batch=True)
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in access this page'
moment = Moment()


def create_app(config_class=Config):
    """
    Factory function that creates an instance of a flask application
    configured and configures it
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login.init_app(app)
    moment.init_app(app)

    # Register created blueprints to the app
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.products import bp as products_bp
    app.register_blueprint(products_bp)

    db.create_all()

    return app


from app import models
