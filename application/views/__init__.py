from flask import current_app
from functools import wraps


def token_required(f):
    @wraps(f)

    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        
        if not token:
            return jsonify({'message' : 'token is missing'}), 401

        try: 
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = User.query.filter_by(_id=data['_id']).first()

        except:
            return jsonify({'message' : 'invalid token'}), 401


        return f(current_user, *args, **kwargs)

    return decorated
