import re
from functools import wraps
from flask import request, jsonify


def validate_uuid(uuid_string: str) -> bool:
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    return bool(uuid_pattern.match(uuid_string))


def require_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': 'Content-Type must be application/json',
                    'details': None
                }
            }), 400
        return f(*args, **kwargs)
    return decorated_function
