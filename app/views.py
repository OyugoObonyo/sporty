from app import app


@app.route('/')
@app.route('/index', strict_slashes=False)
def index():
    return "Simple Page"
