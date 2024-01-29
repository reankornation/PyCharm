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

