from .. import db
from . import user, product

products_likes = db.Table('product_x_user',
    db.Column('user_id', db.Integer, db.ForeignKey('users._id')),
    db.Column('product_id', db.Integer, db.ForeignKey('products._id'))
)

products_bought = db.Table('user_shopping',
    db.Column('user_id', db.Integer, db.ForeignKey('users._id')),
    db.Column('product_id', db.Integer, db.ForeignKey('products._id')),
    db.Column('product_qty', db.Integer, nullable=False, default=1)
)
