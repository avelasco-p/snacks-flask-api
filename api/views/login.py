from flask import (
    Blueprint, redirect, render_template, request, url_for, jsonify, make_response, current_app
)

from werkzeug.security import check_password_hash, generate_password_hash
import uuid
import jwt
import datetime

from ..models.user import User
from .. import db


#creating blueprint
bp = Blueprint('login', __name__, url_prefix='/')


@bp.route('/login', methods=['POST'])
def login():

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="No user found!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({
            'public_id' : user.public_id, 
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=60)
        }, current_app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')}), 202


    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


@bp.route('/register', methods=('GET', 'POST'))
def register():
    data = request.get_json()

    if not data:
        return jsonify({'message' : 'expected json data'}), 400

    if request.method == 'POST':
        user = data['username']
        password = data['password']

        if not user:
            return jsonify({'message' : 'The JSON is not valid'}), 400

        if not password:
            return jsonify({'message' : 'The JSON is not valid'}), 400

        hashed_password = generate_password_hash(password, method='sha256')


        new_user = User(public_id=str(uuid.uuid4()), username=user, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'new user created'}), 201
