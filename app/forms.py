from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SelectField, SubmitField, EmailField
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Regexp, Email
from wtforms.validators import Length

from app.models import User


class TodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    status = SelectField('Status', choices=[(0, 'Todo'), (1, 'In Progress'), (2, 'Done')], coerce=int, default=0)


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[Length(min=4, max=25, message="Це поле має бути довжиною між 4 та 25 символів"),
                                       DataRequired(message="Це поле обов 'язкове"),
                                       Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'username must contain only letters, numbers, underscore and a dot')])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6, message="Це поле має бути більше 6 символів"),
                                                     DataRequired(message="Це поле обов'язкове")])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[Length(min=6, message="Це поле має бути більше 6 символів"),
                                                 DataRequired(message="Це поле обов'язкове"), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, field):
        user = User.query.filter(User.email == field.data).first()
        if user:
            raise ValidationError("User with same email exists")

    def validate_username(self, field):
        user = User.query.filter(User.username == field.data).first()
        if user:
            raise ValidationError("User with same username exists")


"""username = StringField( 'Username
validators-[Length(min=4, max=25,
message = "Це поле має бути довжиною між 4 та 25 символів"),
DataRequired(message = "Це поле обов 'язкове")])
email = StringField('Email', validators- [DataRequired() , Email()])
password = PasswordField('Password'
validators= [Length(min=6,
message = "Це поле має бути більше 6 символів"),
DataRequired (message = "Це поле обов 'язкове"
") 1)
confirm_password = PasswordField('Confirm Password',
validators=[DataRequired(), EqualTo('password')1)"""


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')
