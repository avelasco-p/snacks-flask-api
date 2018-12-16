import os
import click

from flask import Flask, jsonify, request
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure flask app

    app = Flask(__name__, instance_relative_config=True)

    #app configuration loaded
    app.config.from_object('config')
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the intsance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError as e:
        pass

    #adding init db command to app
    app.cli.add_command(init_db)

    #initializing database
    db.init_app(app)

    #importing routes
    from .views import users, login, products, likes,buys
    app.register_blueprint(users.bp, url_prefix='/api/users')
    app.register_blueprint(login.bp, url_prefix='/api')
    app.register_blueprint(products.bp, url_prefix='/api/products')
    app.register_blueprint(likes.bp, url_prefix='/api/likes')
    app.register_blueprint(buys.bp, url_prefix='/api/buys')

    return app


@click.command('init-db')
@with_appcontext
def init_db():
    db.drop_all()
    db.create_all()
    click.echo('Initialized the database.')
