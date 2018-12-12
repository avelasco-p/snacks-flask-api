import os

from flask import Flask


def create_app(test_config=None):
    # create and configure flask app

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

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


    @app.route('/')
    def indexRoute():
        return 'index'

    return app

