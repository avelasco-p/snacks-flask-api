from flask import (
    Blueprint, redirect, render_template, request, url_for, jsonify, make_response, current_app
)

from . import token_required
from ..models.user import User
from ..models.product import Product
from .. import db
from ..models.associations import products_bought

#creating blueprint
bp = Blueprint('buys', __name__, url_prefix='/api/buys')

@bp.route('', methods=['PUT', 'PATCH'])
@token_required
def buy_products(current_user):

    data = request.get_json()

    products_shop = data.get('products', [])

    if not products_shop:
        return jsonify({'message' : 'The JSON is invalid'}), 400

    for product_shopped in products_shop:
        product_p_id = product_shopped.get('public_id', None)
        product_qty = product_shopped.get('quantity', 1)

        if product_p_id:
            product = Product.query.filter_by(public_id=product_p_id).first()

            if product.stock >= product_qty:
                product.stock -= product_qty
                
                # current_user.products_bought.append(product)

                statement = products_bought.insert().values(user_id=current_user._id, product_id=product._id, product_qty=product_qty)
                db.session.execute(statement)

                db.session.commit()
            else:
                return jsonify({'message': 'product out of stock for {}'.format(product_qty)})
        else:
            return jsonify({'message': 'The JSON is invalid'}), 400
        
    return jsonify({'message' : 'products bought successfuly'}), 200


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

        # current_user.products_bought.append(product)
        statement = products_bought.insert().values(user_id=current_user._id, product_id=product._id, product_qty=qty)
        db.session.execute(statement)

        db.session.commit()

        return jsonify({'message' : 'product bought'}), 200

    return jsonify({'message' : 'product out of stock for quantity {}'.format(qty)}), 400
