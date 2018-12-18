from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from ..models.user import User
from .. import db
from . import token_required, admin_required

bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/')
@token_required
@admin_required
def get_all_users(current_user):

    if not current_user:
        return jsonify({'message' : 'The token provided is not authenticated in the api'}), 401

    users = User.query.all()

    lusers = []

    for user in users:
        lproducts_liked = []
        lproducts_bought = []
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['admin'] = user.isAdmin

        for product_liked in user.products_liked:
            product_liked_data = {}
            product_liked_data['public_id'] = product_liked.public_id
            product_liked_data['name'] = product_liked.name

            lproducts_liked.append(product_liked_data)

        for product_bought in user.products_bought:
            product_bought_data = {}
            product_bought_data['public_id'] = product_bought.public_id
            product_bought_data['name'] = product_bought.name

            lproducts_bought.append(product_bought_data)

            
        user_data['products_liked'] = lproducts_liked
        user_data['products_bought'] = lproducts_bought

        lusers.append(user_data)

    return jsonify({'users': lusers}), 200


@bp.route('/<user_public_id>')
@token_required
@admin_required
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


    return jsonify({"message" : "user with public id: {0} not found".format(user_public_id)}), 404


@bp.route('/<user_public_id>', methods=["PUT", "PATCH"])
@token_required
@admin_required
def update_user(current_user, user_public_id):

    data = request.get_json()

    user = User.query.filter_by(public_id=user_public_id).first()

    if user and data:
        try:
            username = data.get('username', None)
            password = data.get('password', None)
            admin = data.get('admin', None)
            products_liked = data.get('products_liked', None)

            if password:
                hashed_password = generate_password_hash(password, method='sha256')
                
            user.username = username if username else user.username
            user.password = hashed_password if password else user.password
            user.isAdmin = admin if admin else user.isAdmin
            user.products_liked = products_liked if products_liked else user.products_liked

            db.session.commit()

            return jsonify({"message" : "user {0} updated".format(user_public_id)}), 200

        except Exception as e:
            print('couldnt update')
            print(e)

    return jsonify({"message" : "user with public id: {0} not found".format(user_public_id)}), 404


@bp.route('/<user_public_id>', methods=["DELETE"])
@token_required
@admin_required
def delete_user(current_user, user_public_id):

    user = User.query.filter_by(public_id=user_public_id).first()

    if user:
        try:
            db.session.delete(user)
            db.session.commit()

            return jsonify({"message" : "user {0} deleted".format(user_public_id)}), 204
        except Exception as e:
            print('couldnt update')
            print(e)

    return jsonify({"message" : "user with public id: {0} not found".format(user_public_id)}), 404
