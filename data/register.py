from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField, TextAreaField, SubmitField, BooleanField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    employment = SelectField('Кем Вы являетесь?', choices=[('Рабочий', 'Рабочий'), ('Работодатель', 'Работодатель')])
    info = TextAreaField('Доп. информация')
    submit = SubmitField('Готово')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Готово')
