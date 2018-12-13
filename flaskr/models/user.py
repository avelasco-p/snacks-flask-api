from flask import current_app
from flas_sqlalchemy import SQLAlchemy


db = SQLAlchemy(current_app)

class User(db.Model):
    """User schema """
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    isAdmin = db.Column(db.Boolean)
