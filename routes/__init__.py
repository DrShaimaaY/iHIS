from flask import Blueprint

auth = Blueprint('auth', __name__)

from routes import auth_routes