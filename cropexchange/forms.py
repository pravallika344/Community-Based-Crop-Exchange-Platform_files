from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, FloatField, IntegerField, FileField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.validators import DataRequired, NumberRange

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=150)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    role = SelectField("Role", choices=[('farmer', 'Farmer'), ('buyer', 'Buyer')], validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")   



class ProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    price = FloatField("Price (₹)", validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=1)])
    image = FileField("Product Image", validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'],'Only image files are allowed!')])
    submit = SubmitField("Add Product")

class OrderForm(FlaskForm):
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Place Order")
