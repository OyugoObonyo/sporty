from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    """
    Form filled in when user intends to post a product
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    image = FileField('Image', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])
    brand = StringField('Brand', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    submit = SubmitField('Publish product')
