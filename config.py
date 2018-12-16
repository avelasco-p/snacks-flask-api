import os

DEBUG=False
SECRET_KEY='dev'
SQL_ALCHEMY_ECHO=False
SQLALCHEMY_DATABASE_URI='sqlite:///{}'.format(os.path.join(os.path.dirname(__file__), 'snacks.db')) 
SQLALCHEMY_TRACK_MODIFICATIONS=True
