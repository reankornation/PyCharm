from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import EmailField, StringField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length, Email

from app.models import User


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
