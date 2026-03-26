from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class Register(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_repeat = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = PasswordField('Фамилия', validators=[DataRequired()])
    name = PasswordField('Имя', validators=[DataRequired()])
    age = PasswordField('Возраст', validators=[DataRequired()])
    position = PasswordField('Позиция', validators=[DataRequired()])
    speciality = PasswordField('Специализация', validators=[DataRequired()])
    address = PasswordField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Войти')
