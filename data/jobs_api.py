import flask
import requests
from flask import render_template, request
from flask_login import current_user, login_required
from flask_restful import abort
from werkzeug.utils import redirect

from data import db_session
from data.users import User
from data.jobs import Jobs, JobsForm, AddressJob
from data.show_map import show, sort_address_jobs, sort_salary_jobs, sort_date_jobs

blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route("/", methods=['GET', 'POST'])
def index():
    form = AddressJob()
    session = db_session.create_session()
    jobs = None
    image = show()
    if request.method == "POST":
        if form.submit_address.data and form.my_address.data != '':
            jobs = sort_address_jobs(form.my_address.data)
        elif form.submit_sort.data:
            form.my_address.data = ''
            if form.sorting.data == 'salary_sort_up':
                jobs = sort_salary_jobs('up')
            elif form.sorting.data == 'salary_sort_down':
                jobs = sort_salary_jobs('down')
            elif form.sorting.data == 'date_sort_up':
                jobs = sort_date_jobs('up')
            elif form.sorting.data == 'date_sort_down':
                jobs = sort_date_jobs('down')
    if jobs is None:
        jobs = session.query(Jobs).all()
    users = session.query(User).all()
    return render_template("index.html", jobs=jobs, users=users, image=image, form=form)


@blueprint.route("/myjobs")
def myjobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).filter(Jobs.employer == current_user.id, Jobs.is_finished == False).all()
    jobs_done = session.query(Jobs).filter(Jobs.employer == current_user.id, Jobs.is_finished == True).all()
    return render_template("my_jobs.html", jobs=jobs, jobs_done=jobs_done)


@blueprint.route('/addjob', methods=['GET', 'POST'])
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

        address = form.address.data
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": address,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]
            jobs.coords = toponym["Point"]["pos"]

        current_user.job.append(jobs)
        session.merge(current_user)
        session.commit()
        return redirect('/myjobs')
    return render_template('jobs.html', title='Добавление работы',
                           form=form)


@blueprint.route('/addjob/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    form = JobsForm()
    if request.method == "GET":
        session = db_session.create_session()
        job = session.query(Jobs).filter(Jobs.id == job_id, Jobs.employer == current_user.id).first()
        if job:
            form.description.data = job.description
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
            job.address = form.address.data
            job.salary = form.salary.data
            job.date = form.date.data
            job.info = form.info.data
            job.is_finished = form.is_finished.data

            address = form.address.data
            geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
            geocoder_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": address,
                "format": "json"}
            response = requests.get(geocoder_api_server, params=geocoder_params)
            if response:
                json_response = response.json()
                toponym = json_response["response"]["GeoObjectCollection"][
                    "featureMember"][0]["GeoObject"]
                job.coords = toponym["Point"]["pos"]

            session.commit()
            return redirect('/myjobs')
        else:
            abort(404)
    return render_template('edit_job.html', title='Редактирование работы', form=form)


@blueprint.route('/job_delete/<int:job_id>', methods=['GET', 'POST'])
@login_required
def job_delete(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == job_id, Jobs.employer == current_user.id).first()
    if job:
        session.delete(job)
        session.commit()
    else:
        abort(404)
    return redirect('/myjobs')
