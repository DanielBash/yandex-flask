from flask import Flask, redirect, url_for
from flask import render_template
from werkzeug.security import generate_password_hash

from data import db_session
from data.jobs import Jobs
from data.users import User
from forms import Register

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def index():
    session = db_session.create_session()
    data = session.query(Jobs).all()
    data_2 = []
    for i in data:
        i.team_leader = session.get(User, i.team_leader).name
        data_2.append(i)
    return render_template('index.html', data=data_2)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=int(form.age.data),
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.username.data,
            hashed_password=generate_password_hash(form.password.data)
        )

        session.add(user)
        session.commit()
        session.close()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


def main():
    app.run()


if __name__ == '__main__':
    db_session.global_init('db/database.sqlite3')
    main()
