from flask import (
    Blueprint, redirect, render_template, request, url_for, jsonify, make_response, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from ..models.user import User
from .. import db
import jwt
import datetime


#creating blueprint
bp = Blueprint('login', __name__, url_prefix='/')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    data = request.get_json()

    if not data:
        return jsonify({'message' : 'expected json data'})

    if request.method == 'POST':
        username = data['username']
        password = data['password']

        if not username:
            return jsonify({'message' : 'no username in data provided'})

        if not password:
            return jsonify({'message' : 'no username in data provided'})

        hashed_password = generate_password_hash(password, method='sha256')


        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'new user created'})


@bp.route('/login', methods=('GET', 'POST'))
def login():
    #get should return template for logging in
    #post should check for user and return jwt if successful

    if request.method == 'GET':
        #get method
        return jsonify({ 'message' : 'authentication form display' })
    else:
        #post method
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

        user = User.query.filter_by(username=auth.username).first()

        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="No user found!"'})

        if check_password_hash(user.password, auth.password):
            token = jwt.encode({
                'id' : user._id, 
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }, current_app.config['SECRET_KEY'])

            return jsonify({'token' : token.decode('UTF-8')}) 


        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
