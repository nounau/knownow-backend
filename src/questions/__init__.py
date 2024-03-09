from flask import Blueprint

bp = Blueprint('questions', __name__)

from src.questions import routes