from flask import Blueprint

bp = Blueprint('answers', __name__)

from app.answers import routes