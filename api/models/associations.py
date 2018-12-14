from .. import db
from . import user, product

products_likes = db.Table('product_x_user',
    db.Column('user_id', db.Integer, db.ForeignKey('users._id'), primary_key = True),
    db.Column('product_id', db.Integer, db.ForeignKey('products._id'), primary_key = True)
)
