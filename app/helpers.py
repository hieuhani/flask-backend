from functools import wraps
from flask import request, jsonify
from werkzeug.exceptions import BadRequest


def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            request.json
        except BadRequest:
            return jsonify({'message': 'Invalid json request'}), 400
        return f(*args, **kw)
    return wrapper
