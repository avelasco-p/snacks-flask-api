from flask import current_app
from flas_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy(current_app)

class User(db.Model):
    """User schema """
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    isAdmin = db.Column(db.Boolean)

    def __init__(self, name, password, isAdmin=False):
        self.name = name;
        self.password = generate_password_hash(password)
        self.isAdmin = isAdmin

