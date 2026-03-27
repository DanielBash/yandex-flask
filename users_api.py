import flask
from flask import jsonify, make_response, request

from data import db_session
from data.users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    sess = db_session.create_session()
    users = sess.query(User).all()
    return jsonify({
        'users': [
            item.to_dict(
                only=(
                    'id', 'surname', 'name', 'age', 'position', 'speciality',
                    'address', 'email', 'modified_date'
                )
            ) for item in users
        ]
    })


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    sess = db_session.create_session()
    user = sess.get(User, user_id)
    sess.close()
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({
        'user': user.to_dict(
            only=(
                'id', 'surname', 'name', 'age', 'position', 'speciality',
                'address', 'email', 'modified_date'
            )
        )
    })


@blueprint.route('/api/users/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    sess = db_session.create_session()
    user = sess.get(User, user_id)
    if not user:
        sess.close()
        return make_response(jsonify({'error': 'Not found'}), 404)
    sess.delete(user)
    sess.commit()
    sess.close()
    return make_response(jsonify({'success': 'Nice'}), 200)


@blueprint.route('/api/users/add', methods=['POST'])
def add_user():
    try:
        sess = db_session.create_session()

        if not request.args.get('email') or not request.args.get('hashed_password'):
            sess.close()
            return make_response(
                jsonify({'error': 'Missing email or password'}), 400
            )

        user = User(
            surname=request.args.get('surname'),
            name=request.args.get('name'),
            age=request.args.get('age', type=int),
            position=request.args.get('position'),
            speciality=request.args.get('speciality'),
            address=request.args.get('address'),
            email=request.args['email'],
            hashed_password=request.args['hashed_password']
        )

        sess.add(user)
        sess.commit()
        sess.close()

        return make_response(jsonify({'success': 'Action completed'}), 200)
    except Exception as e:
        sess.close()
        return make_response(jsonify({'error': 'Action failed'}), 400)


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    sess = db_session.create_session()
    user = sess.get(User, user_id)
    if not user:
        sess.close()
        return make_response(jsonify({'error': 'Not found'}), 404)

    try:
        if 'surname' in request.args:
            user.surname = request.args['surname']
        if 'name' in request.args:
            user.name = request.args['name']
        if 'age' in request.args:
            user.age = request.args.get('age', type=int)
        if 'position' in request.args:
            user.position = request.args['position']
        if 'speciality' in request.args:
            user.speciality = request.args['speciality']
        if 'address' in request.args:
            user.address = request.args['address']
        if 'email' in request.args:
            user.email = request.args['email']
        if 'hashed_password' in request.args:
            user.hashed_password = request.args['hashed_password']

        sess.commit()
        sess.close()
        return make_response(jsonify({'success': 'Action completed'}), 200)
    except Exception as e:
        sess.rollback()
        sess.close()
        return make_response(jsonify({'error': 'Action failed'}), 400)