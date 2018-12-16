from flask import (
    Blueprint, redirect, render_template, request, url_for, jsonify, make_response, current_app
)

from . import token_required
from ..models.user import User
from ..models.product import Product
from .. import db

#creating blueprint
bp = Blueprint('buys', __name__, url_prefix='/api/buys')

# @bp.route('')
# @token_required
# def buy_products(current_user)


@bp.route('/<public_product_id>', methods=['PUT', 'PATCH'])
@token_required
def buy_one_product(current_user, public_product_id):

    data = request.get_json()

    qty = data.get('quantity', 1)

    if not data:
        return jsonify({'message': 'The JSON is not valid'}), 400

    product = Product.query.filter_by(public_id=public_product_id).first()

    #adding product to list of products_bought
    if product.stock >= qty:
        product.stock -= qty
        current_user.products_bought.append(product)

        db.session.commit()

        return jsonify({'message' : 'product bought'}), 200

    return jsonify({'message' : 'product out of stock for quantity {}'.format(qty)}), 400
