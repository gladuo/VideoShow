from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentication, videos, shows, users, comments, errors