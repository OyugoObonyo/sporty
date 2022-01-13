from flask import Blueprint

bp = Blueprint('products', __name__, template_folder='templates')

from app.products import views