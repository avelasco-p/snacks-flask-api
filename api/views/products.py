from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
import uuid

from ..models.product import Product
from .. import db
from . import token_required, admin_required

bp = Blueprint('products', __name__, url_prefix='/products/')


@bp.route('/', methods=["GET"])
def get_all_products():
    products = Product.query.all()

    lproducts = []

    for product in products:
        product_data = {}
        product_data['public_id'] = product.public_id
        product_data['name'] = product.name
        product_data['price'] = product.price
        product_data['stock'] = product.stock_qty

        lproducts.append(product_data)

    return jsonify({'products': lproducts}), 200


@bp.route('/', methods=["POST"])
@token_required
@admin_required
def create_product(current_user):

    data = request.get_json()

    if not data:
        return jsonify({'message' : 'expected json data'}), 400

    try:
        name = data.get('name', None)
        price = data.get('price', None)
        stock = data.get('stock', 0)

        if not name:
            return jsonify({'message' : 'no name provided for product'}), 400

        if not price:
            return jsonify({'message' : 'no price provided for product'}), 400

        if price < 0 :
            return jsonify({'message' : 'price has to be positive (in cents of dollar)'}), 400

        
        new_product = Product(public_id=str(uuid.uuid4()), name=name, price=price, stock_qty=stock)

        db.session.add(new_product)
        db.session.commit()
        

        return jsonify({'message' : 'product created'}), 201
    except Exception as e:
        print(e) 
        return jsonify({'message' : e}), 400


@bp.route('/<product_public_id>', methods=["GET"])
def get_product_by_public_id(current_user, product_public_id):

    product = Product.query.filter_by(public_id=product).first()

    if product:
        product_data = {}
        product_data['public_id'] = product.public_id
        product_data['name'] = product.name
        product_data['price'] = round(product.price / 100)
        product_data['stock'] = product.stock_qty

        return jsonify({"product" : product_data})


    return jsonify({"message" : "product with public id: {0} not found".format(product_public_id)}), 404


@bp.route('/<product_public_id>', methods=["PATCH"])
@token_required
@admin_required
def update_product(current_user, product_public_id):

    data = request.get_json()

    product = Product.query.filter_by(public_id=product_public_id).first()

    if product and data:
        try:
            name = data.get('name', None)
            price = data.get('price', None)
            stock = data.get('stock', None)

            product.name = name if name else product.name
            product.price = round(price / 100) if price else product.price
            product.stock_qty = stock if stock else product.stock_qty

            product_obj = {}
            product_obj['name'] = product.name
            product_obj['price'] = product.price
            product_obj['stock'] = product.stock_qty

            db.session.commit()

            return jsonify({"message" : "product {0} updated".format(product_public_id)}), 200

        except Exception as e:
            print('couldnt update')
            print(e)

    return jsonify({"message" : "body data or product with public id: {0} not found".format(product_public_id)}), 404


@bp.route('/<product_public_id>', methods=["DELETE"])
@token_required
@admin_required
def delete_product(current_user, product_public_id):

    product = Product.query.filter_by(public_id=product_public_id).first()

    if product:
        try:
            db.session.delete(product)
            db.session.commit()

            return jsonify({"message" : "product {0} deleted".format(product_public_id)}), 200
        except Exception as e:
            print('couldnt update')
            print(e)

    return jsonify({"message" : "product with public id: {0} not found".format(product_public_id)}), 404
