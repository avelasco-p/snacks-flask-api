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

    product = Product.query.filter_by(public_id=public_product_id).first()

    if product not in current_user.products_liked:
        #adding product to list of products_liked
        current_user.products_liked.append(product)
        product.popularity += 1
        db.session.commit()

        return jsonify({'message' : 'product liked'}), 200

    return jsonify({'message' : 'product already liked'}), 200
