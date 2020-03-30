import datetime
import sqlalchemy
from flask_wtf import FlaskForm
from sqlalchemy import orm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired

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
    user = orm.relation('User')


class JobsForm(FlaskForm):
    description = StringField("Краткое описание работы", validators=[DataRequired()])
    employer = IntegerField("id нанимателя")
    salary = IntegerField("Оплата за услугу (в рублях)", validators=[DataRequired()])
    address = TextAreaField("Адрес", validators=[DataRequired()])
    info = TextAreaField("Доп. информация")
    coords = TextAreaField("Координаты")
    date = TextAreaField("Дата и время, когда нужно прийти", validators=[DataRequired()])
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
