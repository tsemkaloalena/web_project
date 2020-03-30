import sys

import requests
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


def main():
    @app.route("/test")
    def test():
        db_session.global_init("db/jobs.db")
        session = db_session.create_session()
        points = session.query(Jobs.coords, Jobs.id).all()
        ids = [el[1] for el in points]
        points = [el[0] for el in points]
        points = [f'{points[i].split()[0]},{points[i].split()[1]},pm2ywl{ids[i]}' for i in range(len(points))]
        map_request = f"http://static-maps.yandex.ru/1.x/?&l=map&pt={'~'.join(points)}"
        response = requests.get(map_request)
        map_file = 'static/img/map.png'
        if response:
            with open(map_file, "wb") as file:
                file.write(response.content)
        return render_template('test.html', image=map_file)

    @app.route("/tests")
    def tests():
        db_session.global_init("db/jobs.db")
        session = db_session.create_session()
        jobs = session.query(Jobs).all()

        address = 'Москва, Большая Академическая, 22'
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
            coodrinates = toponym["Point"]["pos"]

            sp = [(job, ((float(job.coords.split()[0]) - float(coodrinates.split()[0])) ** 2 + (
                    float(job.coords.split()[1]) - float(coodrinates.split()[1])) ** 2) ** 0.5) for job in jobs]
            sp = [el[0] for el in sorted(sp, key=lambda x: x[1])]




        return render_template('test.html')


if __name__ == '__main__':
    main()
    app.run()
