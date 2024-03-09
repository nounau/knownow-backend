from flask import Blueprint

bp = Blueprint('answers', __name__)

from src.answers import routes