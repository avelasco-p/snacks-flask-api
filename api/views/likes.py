from flask import (
    Blueprint, redirect, render_template, request, url_for, jsonify, make_response, current_app
)

from . import token_required
from ..models.user import User
from ..models.product import Product
from .. import db


#creating blueprint
bp = Blueprint('likes', __name__, url_prefix='/api/likes')


@bp.route('/<public_product_id>', methods=['POST'])
@token_required
def like_one_product(current_user, public_product_id):
    print(public_product_id)
    print(current_user.products_liked)

    if public_product_id not in current_user.products_liked:
        db.session.commit()

        # print(current_user.products_liked)

        return jsonify({'message' : 'product liked'}), 200

    return jsonify({'message' : 'product already liked'}), 200
