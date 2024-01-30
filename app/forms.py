from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import PasswordField, BooleanField, SelectField
from wtforms import StringField, EmailField, SubmitField
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from wtforms.validators import EqualTo, Regexp

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


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class ChangePassword(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired('old password is required')])
    new_password = PasswordField('New Password', validators=[DataRequired('new password is required')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired('confirm password is required'), EqualTo('password')])


class UpdateAccountForm(FlaskForm):
    new_username = StringField('Change username', validators=[DataRequired(), Length(min=4, max=25)])
    new_email = EmailField('Change email', validators=[DataRequired(), Email()])
    profile_picture = FileField('Update Profile Picture',
                                validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only! Please upload a valid image.')
    ])
    about_me = TextAreaField('About me')

    def validate_new_email(self, field):
        user = User.query.filter(User.email == field.data).first()
        if user and user.id != current_user.id:
            raise ValidationError("Email is already in use by another user.")

    def validate_new_username(self, field):
        user = User.query.filter(User.username == field.data).first()
        if user and user.id != current_user.id:
            raise ValidationError("Username is already in use by another user.")
