from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from ..models.user import User
from .. import db

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/', methods=['GET'])
def get_all_users():
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['id'] = user._id
        user_data['username'] = user.username
        user_data['isAdmin'] = user.isAdmin
        user_data['products_liked'] = user.product_likes

        output.append(user_data)

    return jsonify({'users': output})
