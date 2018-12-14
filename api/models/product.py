from flask_sqlalchemy import SQLAlchemy
from .. import db


class Product(db.Model):
    """User schema """
    __tablename__ = 'products'
    _id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Integer) #in cents of dollar
    stock_qty = db.Column(db.Integer)
