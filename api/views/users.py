from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from ..models.user import User
from .. import db
from . import token_required, admin_required

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/')
@token_required
@admin_required
def get_all_users(admin, current_user):
    users = User.query.all()

    lusers = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['admin'] = user.isAdmin
        user_data['products_liked'] = user.products_liked

        lusers.append(user_data)

    return jsonify({'users': lusers})

@bp.route('/<user_public_id>')
@token_required
def get_user_by_public_id(current_user, user_public_id):

    user = User.query.filter_by(public_id=user_public_id).first()

    if user:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['admin'] = user.isAdmin
        user_data['products_liked'] = user.products_liked

        return jsonify({"user" : user_data})


    return jsonify({"message" : "user with public id: {0} not found".format(user_public_id)})
