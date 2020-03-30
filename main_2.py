from flask_restful import abort
from werkzeug.utils import redirect

from data import db_session
from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from data.users import User
from data.jobs import Jobs, JobsForm
from data.register import LoginForm, RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you_will_never_pass_my_password'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/jobs.db")

    @login_manager.user_loader
    def load_user(user_id):
        session = db_session.create_session()
        return session.query(User).get(user_id)

    @app.route('/login', methods=['GET', 'POST'])
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

    @app.route("/")
    def index():
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return render_template("index.html", jobs=jobs)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    @app.route('/register', methods=['GET', 'POST'])
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
            session = db_session.create_session()
            session.add(user)
            session.commit()
            return redirect('/')
        return render_template('register.html', title='Register',
                               form=form)

    @app.route('/addjob', methods=['GET', 'POST'])
    @login_required
    def add_job():
        form = JobsForm()
        if form.validate_on_submit():
            session = db_session.create_session()
            jobs = Jobs()
            jobs.description = form.description.data
            jobs.employer = current_user
            jobs.address = form.address.data
            jobs.salary = form.salary.data
            jobs.date = form.date.data
            jobs.info = form.info.data
            jobs.is_finished = form.is_finished.data
            current_user.job.append(jobs)
            session.merge(current_user)
            session.commit()
            return redirect('/')
        return render_template('jobs.html', title='Добавление работы',
                               form=form)

    @app.route('/addjob/<int:job_id>', methods=['GET', 'POST'])
    @login_required
    def edit_job(job_id):
        form = JobsForm()
        if request.method == "GET":
            session = db_session.create_session()
            job = session.query(Jobs).filter(Jobs.id == job_id, Jobs.employer == current_user.id).first()
            if job:
                form.description.data = job.description
                # form.employer.data = current_user
                form.address.data = job.address
                form.salary.data = job.salary
                form.date.data = job.date
                form.info.data = job.info
                form.is_finished.data = job.is_finished
            else:
                abort(404)
        if form.validate_on_submit():
            session = db_session.create_session()
            job = session.query(Jobs).filter(Jobs.id == job_id, Jobs.employer == current_user.id).first()
            if job:
                job.description = form.description.data
                # job.employer = current_user
                job.address = form.address.data
                job.salary = form.salary.data
                job.date = form.date.data
                job.info = form.info.data
                job.is_finished = form.is_finished.data
                session.commit()
                return redirect('/')
            else:
                abort(404)
        return render_template('jobs.html', title='Редактирование работы', form=form)

    @app.route('/job_delete/<int:job_id>', methods=['GET', 'POST'])
    @login_required
    def job_delete(job_id):
        session = db_session.create_session()
        job = session.query(Jobs).filter(Jobs.id == job_id, Jobs.employer == current_user.id).first()
        if job:
            session.delete(job)
            session.commit()
        else:
            abort(404)
        return redirect('/')


if __name__ == '__main__':
    main()
    app.run()
