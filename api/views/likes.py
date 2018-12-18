from flask import (
    Blueprint, redirect, render_template, request, url_for, jsonify, make_response, current_app
)

from . import token_required
from ..models.user import User
from ..models.product import Product
from .. import db

#creating blueprint
bp = Blueprint('likes', __name__, url_prefix='/api/likes')

@bp.route('', methods=['PUT', 'PATCH'])
@token_required
def buy_products(current_user):

    if not current_user:
        return jsonify({'message' : 'The token provided is not authenticated in the api'}), 401

    data = request.get_json()

    products_liked = data.get('products', [])

    if not products_liked:
        return jsonify({'message' : 'The JSON is invalid'}), 400

    for product_liked in products_liked:
        product_p_id = product_liked.get('public_id', None)

        if product_p_id:
            product = Product.query.filter_by(public_id=product_p_id).first()

            if product not in current_user.products_liked:
                product.popularity += 1
                current_user.products_liked.append(product)

        else:
            return jsonify({'message': 'Product not found'}), 404

    db.session.commit()

    return jsonify({'message' : 'products liked successfuly'}), 200


@bp.route('/<public_product_id>', methods=['PUT', 'PATCH'])
@token_required
def like_one_product(current_user, public_product_id):

    if not current_user:
        return jsonify({'message' : 'The token provided is not authenticated in the api'}), 401

    product = Product.query.filter_by(public_id=public_product_id).first()

    if not product:
        return jsonify({'message' : 'Product not found'}), 404

    if product not in current_user.products_liked:
        #adding product to list of products_liked
        product.popularity += 1
        current_user.products_liked.append(product)

        db.session.commit()

        return jsonify({'message' : 'product liked'}), 200

    return jsonify({'message' : 'product already liked'}), 304
