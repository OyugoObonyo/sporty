from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    """
    Form filled in by new users
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """
        Validates form to check whether username already exists in the db
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Sorry, this Username is taken")

    def validate_email(self, email):
        """
        Validates form to check whether email already exists in the db
        """
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError("Sorry, email already exists")


class LoginForm(FlaskForm):
    """
    Form filled in when user wants to log in
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')
