from flask_sqlalchemy import SQLAlchemy
from .. import db
from . import product, associations


class User(db.Model):
    """User schema """
    __tablename__ = 'users'
    _id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)
    products_bought = db.relationship("Product", secondary=associations.products_bought)
    products_liked = db.relationship("Product", secondary=associations.products_likes)
