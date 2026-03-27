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
        'jobs': [item.to_dict(only=('job', 'team_leader ', 'collaborators', 'is_finished', 'start_date', 'end_date'))
                 for item in jobs]
    })


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    sess = db_session.create_session()
    jobs = sess.get(Jobs, job_id)
    sess.close()
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({
        'job': jobs.to_dict(only=('job', 'team_leader ', 'collaborators', 'is_finished', 'start_date', 'end_date'))
    })


@blueprint.route('/api/jobs/delete/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    sess = db_session.create_session()
    jobs = sess.get(Jobs, job_id)
    if not jobs:
        sess.close()
        return make_response(jsonify({'error': 'Not found'}), 404)
    sess.delete(jobs)
    sess.commit()
    sess.close()
    return make_response(jsonify({'success': 'Nice'}), 200)


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
        sess.commit()
        sess.close()
        return make_response(jsonify({'success': 'Action completed'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': 'Action failed'}), 400)


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_job(job_id):
    sess = db_session.create_session()
    job = sess.get(Jobs, job_id)
    if not job:
        sess.close()
        return make_response(jsonify({'error': 'Not found'}), 404)

    try:
        if 'job' in request.args:
            job.job = request.args['job']
        if 'team_leader' in request.args:
            job.team_leader = request.args['team_leader']
        if 'collaborators' in request.args:
            job.collaborators = request.args['collaborators']
        if 'is_finished' in request.args:
            job.is_finished = request.args['is_finished'].lower() == 'true'
        if 'start_date' in request.args:
            job.start_date = request.args['start_date']
        if 'end_date' in request.args:
            job.end_date = request.args['end_date']
        if 'work_size' in request.args:
            job.work_size = int(request.args['work_size'])
        if 'category' in request.args:
            job.category = request.args['category']

        sess.commit()
        sess.close()
        return make_response(jsonify({'success': 'Action completed'}), 200)
    except Exception as e:
        sess.rollback()
        sess.close()
        return make_response(jsonify({'error': 'Action failed'}), 400)