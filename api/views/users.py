from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from ..models.user import User
from .. import db
from . import token_required

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/', methods=['GET'])
@token_required
def get_all_users(current_user):
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['id'] = user._id
        user_data['username'] = user.username
        user_data['admin'] = user.isAdmin
        user_data['products_liked'] = user.products_liked

        output.append(user_data)

    return jsonify({'users': output})
