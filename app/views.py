from werkzeug.utils import redirect
from wtforms.fields.simple import EmailField
from app import app, db
from flask import render_template, flash, url_for
from app.forms import RegistrationForm
from app.models import User

@app.route('/')
@app.route('/index', strict_slashes=False)
def index():
    return render_template('/index.html', title='Home')


@app.route('/register', methods=['GET','POST'] ,strict_slashes=False)
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations! Registration was successful')
        return redirect(url_for('login'))
    return render_template('/register.html', title='Register', form=form)


