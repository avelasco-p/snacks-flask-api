from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, make_response
)
from sqlalchemy import asc, desc, and_, or_
from sqlalchemy.orm import load_only
import uuid

from ..models.product import Product
from .. import db
from . import token_required, admin_required


bp = Blueprint('products', __name__, url_prefix='/api/products')


@bp.route('/', methods=["GET"])
def get_all_products():
    # pagination and sorting settings from params
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 20))
    sort_by = request.args.get('sort', '+name')
    fields = request.args.get('fields', None)
    search = request.args.get('search', None)

    # multiple params from single object
    fields = fields.split(',') if fields else None

    # getting column of model from params
    column_sort_by = getattr(Product, sort_by[1:])

    # query applying all params
    products_count = Product.query.count()
    products_page = Product.query \
        .filter(and_(Product.stock > 0, Product.name.like('%' + search + '%') if search else True)) \
        .order_by(desc(column_sort_by) if sort_by[0] == "-" else asc(column_sort_by)) \
        .with_entities(*fields if fields else Product.__table__.columns) \
        .paginate(page=offset, per_page=limit, error_out=False)

    lproducts = []

    # creating list of products
    for product in products_page.items:
        product_data = {}

        # filtering fields in case of param definition
        if fields:
            for field in fields:
                product_data[field] = getattr(product, field)
        else:
            product_data['public_id'] = product.public_id
            product_data['name'] = product.name
            product_data['price'] = round(float(product.price / 100), 2)
            product_data['stock'] = product.stock
            product_data['popularity'] = product.popularity

        lproducts.append(product_data)

    # headers variable
    res_header = {}

    # setting up headers values
    res_header['Content-Type'] = 'application/json'
    res_header['X-Total-Count'] = products_count

    # setting up pagination link for headers
    pagination_links = [
        '<{}>; rel="first"'.format(request.base_url + '?offset={0}&limit={1}{2}'.format(
            0, limit, '&search=' + search if search else '')),
        '<{}>; rel="last"'.format(request.base_url + '?offset={0}&limit={1}{2}'.format(
            products_page.pages - 1, limit, '&search=' + search if search else ''))
    ]

    if products_page.has_prev:
        pagination_links.append('<{}>; rel="prev"'.format(
            request.base_url + '?offset={0}&limit={1}{2}'.format(offset - 1, limit, '&search=' + search if search else '')))

    if products_page.has_next:
        pagination_links.append('<{}>; rel="next"'.format(
            request.base_url + '?offset={0}&limit={1}{2}'.format(offset + 1, limit, '&search=' + search if search else '')))

    res_header['Link'] = []
    for link in pagination_links:
        res_header['Link'].append(link)

    res = make_response(jsonify({'products': lproducts}), 200)

    res.headers = res_header

    return res


@bp.route('/<product_public_id>', methods=["GET"])
def get_product_by_public_id(product_public_id):
    # param for selecting only some columns
    fields = request.args.get('fields', None)

    # multiple params from single object
    fields = fields.split(',') if fields else None

    product = Product.query \
        .filter_by(public_id=product_public_id) \
        .with_entities(*fields if fields else Product.__table__.columns) \
        .first()

    if product:
        product_data = {}

        if fields:
            for field in fields:
                product_data[field] = getattr(product, field)
        else:
            product_data['public_id'] = product.public_id
            product_data['name'] = product.name
            product_data['price'] = round(product.price / 100)
            product_data['stock'] = product.stock
            product_data['popularity'] = product.popularity

        return jsonify({"product": product_data}), 200

    return jsonify({"message": "product with public id: {0} not found".format(product_public_id)}), 404


@bp.route('', methods=["POST"])
@token_required
@admin_required
def create_product(current_user):

    if not current_user:
        return jsonify({'message' : 'The token provided is not registered in our api, please log in again'}), 401

    data = request.get_json()

    if not data:
        return jsonify({'message': 'expected json data'}), 400

    try:
        name = data.get('name', None)
        price = data.get('price', None)
        stock = data.get('stock', 0)

        if not name:
            return jsonify({
                'message': 'The JSON is invalid',
                'error': 'No name provided in JSON body'
            }), 400

        if not price:
            return jsonify({
                'message': 'The JSON is invalid',
                'error': 'No price provided in JSON body'
            }), 400

        if price < 0:
            return jsonify({
                'message': 'price has to be positive (in cents of dollar)'
            }), 400

        new_product = Product(public_id=str(
                        uuid.uuid4()), name=name, price=price, stock=stock)

        if new_product:
            db.session.add(new_product)
            db.session.commit()
        else:
            return jsonify({
                'message' : 'there was an error creating your product',
                'error' : 'Internal server error'
            }), 500

        return jsonify({'message': 'product created'}), 201
    except Exception as e:
        print(e)
        return jsonify({'message': e}), 400


@bp.route('/<product_public_id>', methods=["PUT"])
@token_required
@admin_required
def replace_product(current_user, product_public_id):

    if not current_user:
        return jsonify({'message' : 'The token provided is not registered in our api, please log in again'}), 401

    data = request.get_json()

    if not data:
        return jsonify({'message': 'The JSON is invalid'}), 400

    try:
        name = data.get('name', None)
        price = data.get('price', None)
        stock = data.get('stock', 0)
        popularity = data.get('popularity', 0)

        if not name:
            return jsonify({
                'message': 'The JSON is invalid',
                'error': 'No name provided in JSON body'
            }), 400

        if not price:
           return jsonify({
                'message': 'The JSON is invalid',
                'error': 'No price provided in JSON body'
            }), 400

        if price < 0:
            return jsonify({
                'message': 'The JSON is invalid',
                'error': 'Price cant be lower than 0'
            }), 400

        product = Product.query \
                            .filter_by(public_id=product_public_id) \
                            .first()

        if not product :
            return jsonify({'message' : 'product with public id {} not found'.format(product_public_id)}), 404

        product.name = name
        product.price = price
        product.stock = stock
        product.popularity = popularity

        db.session.commit()

        return jsonify({'message': 'product data replaced'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': e}), 400


@bp.route('/<product_public_id>', methods=["PATCH"])
@token_required
@admin_required
def update_product(current_user, product_public_id):

    if not current_user:
        return jsonify({'message' : 'The token provided is not registered in our api, please log in again'}), 401

    data = request.get_json()

    product = Product.query.filter_by(public_id=product_public_id).first()

    if product and data:
        try:
            product.name = data.get('name', product.name)
            product.price = data.get('price', product.price)
            product.stock = data.get('stock', product.stock)

            db.session.commit()

            return jsonify({"message": "product {0} updated".format(product_public_id)}), 200

        except Exception as e:
            print('couldnt update')
            print(e)

    return jsonify({
        "message": "body data or product with public id: {0} not found".format(product_public_id)
    }), 404


@bp.route('/<product_public_id>', methods=["DELETE"])
@token_required
@admin_required
def delete_product(current_user, product_public_id):
    
    if not current_user:
        return jsonify({'message' : 'The token provided is not registered in our api, please log in again'}), 401

    product = Product.query.filter_by(public_id=product_public_id).first()

    if product:
        try:
            db.session.delete(product)
            db.session.commit()

            return jsonify({"message": "product {0} deleted".format(product_public_id)}), 204
        except Exception as e:
            print('couldnt update')
            print(e)

    return jsonify({"message": "product with public id: {0} not found".format(product_public_id)}), 404


@bp.route('', methods=["DELETE"])
@token_required
@admin_required
def delete_all_products(current_user):

    all_products = Product.query.all()

    db.session.delete(all_products)
    db.session.commit()

    return jsonify({"message": "products deleted"}), 204
