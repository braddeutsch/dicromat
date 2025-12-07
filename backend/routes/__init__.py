from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

from . import test_routes
from . import slider_routes
