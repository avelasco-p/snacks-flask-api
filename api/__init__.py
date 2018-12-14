import os
import click

from flask import Flask, jsonify, request
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure flask app

    app = Flask(__name__, instance_relative_config=True)

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

    app.cli.add_command(init_db)
    db.init_app(app)

    from .views import users, login, products
    app.register_blueprint(users.bp)
    app.register_blueprint(login.bp)
    app.register_blueprint(products.bp)

    return app


@click.command('init-db')
@with_appcontext
def init_db():
    db.drop_all()
    db.create_all()
    click.echo('Initialized the database.')

