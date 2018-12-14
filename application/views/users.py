from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from ..models.user import User
from .. import db

bp = Blueprint('users', __name__, url_prefix='/users')
