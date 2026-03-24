from flask import Flask
from flask import render_template
from data import db_session
from data.jobs import Jobs
from data.users import User

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


def main():
    app.run()


if __name__ == '__main__':
    db_session.global_init('db/database.sqlite3')
    main()
