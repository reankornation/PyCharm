from wtforms import PasswordField, BooleanField, SelectField
from wtforms.validators import Length
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логін', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=4, max=10)])
    remember = BooleanField('Запамятати мене')


class TodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    status = SelectField('Status', choices=[(0, 'Todo'), (1, 'In Progress'), (2, 'Done')], coerce=int, default=0)
