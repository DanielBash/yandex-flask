import flask
from flask import jsonify, make_response, request

from data import db_session
from data.jobs import Jobs


blueprint = flask.Blueprint(
    'mars_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    sess = db_session.create_session()
    jobs = sess.query(Jobs).all()
    return jsonify({
        'jobs': [item.to_dict(only=('job', 'team_leader ', 'collaborators', 'is_finished', 'start_date', 'end_date')) for item in jobs]
    })


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    sess = db_session.create_session()
    jobs = sess.get(Jobs, job_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({
        'job': jobs.to_dict(only=('job', 'team_leader ', 'collaborators', 'is_finished', 'start_date', 'end_date'))
    })

@blueprint.route('/api/jobs/add', methods=['POST'])
def add_job():
    try:
        sess = db_session.create_session()
        job = Jobs(
            is_finished=request.args['is_finished'],
            job=request.args['job'],
            collaborators=request.args['collaborators'],
            team_leader=request.args['team_leader'],
            work_size=request.args['work_size'],
            category=request.args['category']
        )
        sess.add(job)
        sess.close()
        return make_response(jsonify({'success': 'Action completed'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Action failed'}), 400)