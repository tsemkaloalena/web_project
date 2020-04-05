import datetime

import requests
import sqlalchemy
from flask_wtf import FlaskForm
from sqlalchemy import orm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError

from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    employer = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    description = sqlalchemy.Column(sqlalchemy.String)
    salary = sqlalchemy.Column(sqlalchemy.Integer)
    address = sqlalchemy.Column(sqlalchemy.String)
    info = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.String)
    coords = sqlalchemy.Column(sqlalchemy.String)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    employee = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    user = orm.relation('User')


class JobsForm(FlaskForm):
    def check_address(self, field):
        try:
            geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
            geocoder_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": field.data,
                "format": "json"}
            response = requests.get(geocoder_api_server, params=geocoder_params)
            if response:
                json_response = response.json()
                toponym = json_response["response"]["GeoObjectCollection"][
                    "featureMember"][0]["GeoObject"]["Point"]["pos"]
            else:
                raise ValidationError('invalid address')
        except:
            raise ValidationError('invalid address')

    description = StringField("Краткое описание работы", validators=[DataRequired()])
    employer = IntegerField("id нанимателя")
    salary = IntegerField("Оплата за услугу (в рублях)", validators=[DataRequired()])
    address = TextAreaField("Адрес", validators=[DataRequired(), check_address])
    info = TextAreaField("Доп. информация")
    coords = TextAreaField("Координаты")
    date = TextAreaField("Когда нужно прийти (дата и время)", validators=[DataRequired()])
    is_finished = BooleanField("Выполнена ли работа?")
    submit = SubmitField('Готово')


class AddressJob(FlaskForm):
    sorting = SelectField('Сортировать по', choices=[('date_sort_up', 'дате добавления (от старого к новому)'),
                                                     ('date_sort_down', 'дате добавления (от нового к старому)'),
                                                     ('salary_sort_up', 'оплате труда (по возрастанию)'),
                                                     ('salary_sort_down', 'оплате труда (по убыванию)')])

    my_address = StringField('Ваш адрес')
    submit_address = SubmitField('Найти ближайшие предложения')
    submit_sort = SubmitField('Сортировать')


class Ready(FlaskForm):
    submit_ready = SubmitField('Готов(а, о, ы) приступить к работе')
    submit_refuse = SubmitField('Отказаться')
