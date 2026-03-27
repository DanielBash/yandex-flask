from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.jobs import Jobs


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.get(Jobs, job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")
    session.close()


parser = reqparse.RequestParser()
parser.add_argument('job', type=str, required=True)
parser.add_argument('team_leader', type=int, required=True)
parser.add_argument('collaborators', type=str)
parser.add_argument('is_finished', type=bool)
parser.add_argument('start_date', type=str)
parser.add_argument('end_date', type=str)
parser.add_argument('work_size', type=int)
parser.add_argument('category', type=int)


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.get(Jobs, job_id)
        return jsonify({
            'job': job.to_dict(
                only=('job', 'team_leader', 'collaborators', 'is_finished',
                      'start_date', 'end_date', 'work_size', 'category')
            )
        })

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.get(Jobs, job_id)
        session.delete(job)
        session.commit()
        session.close()
        return jsonify({'success': 'OK'})

    def put(self, job_id):
        abort_if_job_not_found(job_id)
        args = parser.parse_args()
        session = db_session.create_session()
        job = session.get(Jobs, job_id)

        if args['job']:
            job.job = args['job']
        if args['team_leader'] is not None:
            job.team_leader = args['team_leader']
        if args['collaborators']:
            job.collaborators = args['collaborators']
        if args['is_finished'] is not None:
            job.is_finished = args['is_finished']
        if args['start_date']:
            job.start_date = args['start_date']
        if args['end_date']:
            job.end_date = args['end_date']
        if args['work_size'] is not None:
            job.work_size = args['work_size']
        if args['category'] is not None:
            job.category = args['category']

        session.commit()
        session.close()
        return jsonify({'success': 'OK'})

class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({
            'jobs': [item.to_dict(
                only=('job', 'team_leader', 'collaborators', 'is_finished',
                      'start_date', 'end_date', 'work_size', 'category')
            ) for item in jobs]
        })

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            job=args['job'],
            team_leader=args['team_leader'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished'],
            start_date=args['start_date'],
            end_date=args['end_date'],
            work_size=args['work_size'],
            category=args['category']
        )
        session.add(job)
        session.commit()
        session.close()
        return jsonify({'id': job.id})