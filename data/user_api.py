import flask
from flask import Flask, render_template
from flask_login import login_user, login_required, logout_user
from werkzeug.utils import redirect

from data import db_session
from data.jobs import Jobs
from data.register import LoginForm, RegisterForm
from data.users import User
from data.vk_messages import check_id_exist, send_message

blueprint = flask.Blueprint('users_api', __name__, template_folder='templates')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        user.email = form.email.data
        user.set_password(form.password.data)
        user.name = form.name.data
        user.surname = form.surname.data
        user.employment = form.employment.data
        user.info = form.info.data
        if check_id_exist(form.vk_id.data):
            if user.employment == 'Рабочий':
                mes = f'''Глубокоуважаемый Вагоноуважатый {user.name}, 
                          Вы успешно зарегестрировались на нашем сайте!\n\n
                          Теперь вы можете выбрать работу!'''
            else:
                mes = f'''Вагоноуважаемый Глубокоуважатый {user.name}, 
                          Вы успешно зарегестрировались на нашем сайте!\n\n
                          Теперь вы добавить работу!'''
            user.vk_id = form.vk_id.data
            send_message(user.vk_id, mes)
        else:
            user.vk_id = 'None'
        session = db_session.create_session()
        session.add(user)

        session.commit()
        return redirect('/')
    return render_template('register.html', title='Register',
                           form=form)
