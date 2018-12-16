from flask_sqlalchemy import SQLAlchemy
from .. import db


class Product(db.Model):
    """User schema """
    __tablename__ = 'products'
    _id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Integer, nullable=False) #in cents of dollar
    stock = db.Column(db.Integer, default=0)
    popularity = db.Column(db.Integer, nullable=False, default=0)
