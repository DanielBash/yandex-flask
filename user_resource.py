from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.users import User


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")
    session.close()


parser = reqparse.RequestParser()
parser.add_argument('surname', type=str)
parser.add_argument('name', type=str)
parser.add_argument('age', type=int)
parser.add_argument('position', type=str)
parser.add_argument('speciality', type=str)
parser.add_argument('address', type=str)
parser.add_argument('email', type=str, required=True)
parser.add_argument('hashed_password', type=str, required=True)


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.get(User, user_id)
        return jsonify({
            'user': user.to_dict(
                only=('id', 'surname', 'name', 'age', 'position',
                      'speciality', 'address', 'email', 'modified_date')
            )
        })

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.get(User, user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        args = parser.parse_args()
        session = db_session.create_session()
        user = session.get(User, user_id)

        if args['surname']:
            user.surname = args['surname']
        if args['name']:
            user.name = args['name']
        if args['age'] is not None:
            user.age = args['age']
        if args['position']:
            user.position = args['position']
        if args['speciality']:
            user.speciality = args['speciality']
        if args['address']:
            user.address = args['address']
        if args['email']:
            user.email = args['email']
        if args['hashed_password']:
            user.hashed_password = args['hashed_password']

        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({
            'users': [item.to_dict(
                only=('id', 'surname', 'name', 'age', 'position',
                      'speciality', 'address', 'email', 'modified_date')
            ) for item in users]
        })

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            hashed_password=args['hashed_password']
        )
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})