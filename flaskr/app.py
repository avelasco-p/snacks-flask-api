from flask import Flask
app = Flask(__name__)

@app.route('/')
def indexRoute():
    """TODO: Docstring for index.
    :returns: response for index route

    """
    return 'index'

@app.route('/snacks/')
def snacksRoute():
    """TODO: Docstring for snacksRoute.
    :returns: snacks route 

    """
    return 'snacks'
