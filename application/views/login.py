from flask import (
    Blueprint, redirect, render_template, request, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from ..models.user import User
from .. import db


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


        new_user = User(name=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'new user created'})


@bp.route('/login', methods=('GET', 'POST'))
def login():
    #get should return template for logging in
    #post should check for user and return jwt if successful

    data = request.get_json()

    if not data or not data.username or not data.password:
        return jsonify({'message' : 'not enough data provided'}), 401
    
    return jsonify({'method': method})
