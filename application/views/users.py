from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from ..models.user import User

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/')
def get_all_users():
    return jsonify({"message" : "all users here"})


@bp.route('/login', methods=['GET', 'POST'])
def login():
    #get should return template for logging in
    #post should check for user and return jwt if successful
    method = request.method

    if method == 'GET':
        return jsonify({'message' : "insert credentials"})

    elif method == 'POST':
        return jsonify({'data': request.data})

    return jsonify({'method': method})

@bp.route('register', methods=['GET', 'POST'])
def register():
    #get should show template for register

    method = request.method

    if method == 'POST':
        data = request.get_json()

        hashed_password = generate_password_hash(data['password'], method='sha256')

        new_user = User(name=data['name'], password=hashed_password)
        print(g.db)

        return jsonify({"message" : "user created"})

    return jsonify({"message": "error"})
         
