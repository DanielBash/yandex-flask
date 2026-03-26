import datetime

from flask import Flask, redirect, url_for
from flask import render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash

from data import db_session
from data.departments import Department
from data.jobs import Jobs
from data.users import User
from forms import LoginForm, RegisterForm, JobForm, DepartmentForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    us = db_sess.get(User, user_id)
    db_sess.close()
    return us


@app.route('/')
@app.route('/index')
def index():
    session = db_session.create_session()
    data = session.query(Jobs).all()
    data_2 = []
    for i in data:
        i.team_leader = session.get(User, i.team_leader).name
        data_2.append(i)
    session.close()
    return render_template('index.html', data=data_2)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=int(form.age.data),
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
            hashed_password=generate_password_hash(form.password.data)
        )

        session.add(user)
        session.commit()
        session.close()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def addjob():
    form = JobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        job = Jobs(
            is_finished=form.is_finished.data,
            job=form.job.data,
            collaborators=form.collaborators.data,
            team_leader=form.team_leader.data,
            work_size=form.work_size.data,
        )

        session.add(job)
        session.commit()
        session.close()
        return redirect(url_for('index'))
    return render_template('job.html', form=form)


@app.route('/editjob/<int:job_id>', methods=['GET', 'POST'])
@login_required
def editjob(job_id):
    session = db_session.create_session()

    try:
        job = session.get(Jobs, job_id)
        if job.creator_id != current_user.id and job.team_leader != current_user.id:
            return redirect(url_for('index'))
    except Exception as e:
        return redirect(url_for('index'))

    form = JobForm()
    if form.validate_on_submit():
        job.is_finished = form.is_finished.data
        job.job = form.job.data
        job.collaborators = form.collaborators.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.creator_id = current_user.id

        session.commit()
        session.close()
        return redirect(url_for('index'))
    return render_template('job.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/deletejob/<int:job_id>', methods=['GET', 'POST'])
@login_required
def deletejob(job_id):
    session = db_session.create_session()

    try:
        job = session.get(Jobs, job_id)
        if job.creator_id != current_user.id and job.team_leader != current_user.id:
            return redirect(url_for('index'))
        session.delete(job)
        session.commit()
        session.close()
    except Exception as e:
        return redirect(url_for('index'))

    return redirect(url_for('index'))


@app.route('/deletedepartment/<int:department_id>', methods=['GET', 'POST'])
@login_required
def deletedepartment(department_id):
    session = db_session.create_session()

    try:
        job = session.get(Department, department_id)
        if job.creator_id != current_user.id and job.chief != current_user.id:
            return redirect(url_for('departments'))
        session.delete(job)
        session.commit()
        session.close()
    except Exception as e:
        return redirect(url_for('departments'))

    return redirect(url_for('departments'))


@app.route('/adddepartment', methods=['GET', 'POST'])
@login_required
def adddepartment():
    form = DepartmentForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        try:
            dept = Department(
                title=form.title.data,
                chief=form.chief.data,
                members=form.members.data,
                email=form.email.data,
                creator_id=current_user.id,
            )
            session.add(dept)
            session.commit()
            return redirect(url_for('departments'))
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    return render_template('department.html', form=form)


@app.route('/editdepartment/<int:department_id>', methods=['GET', 'POST'])
@login_required
def editdepartment(department_id):
    session = db_session.create_session()
    try:
        dept = session.get(Department, department_id)
        if dept is None:
            return redirect(url_for('departments'))

        if dept.creator_id != current_user.id and dept.cheif != current_user.id:
            return redirect(url_for('departments'))
    except Exception:
        return redirect(url_for('departments'))

    form = DepartmentForm()
    if form.validate_on_submit():
        try:
            dept.title = form.title.data
            dept.chief = form.chief.data
            dept.members = form.members.data
            dept.email = form.email.data

            session.commit()
            return redirect(url_for('departments'))
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    form.title.data = dept.title
    form.chief.data = dept.chief
    form.members.data = dept.members
    form.email.data = dept.email

    return render_template('department.html', form=form)


@app.route('/departments')
def departments():
    session = db_session.create_session()
    data = session.query(Department).all()
    session.close()
    return render_template('departments.html', data=data)


def main():
    app.run()


if __name__ == '__main__':
    db_session.global_init('db/database.sqlite3')
    main()
