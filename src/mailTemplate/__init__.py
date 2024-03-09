from flask import Blueprint

bp = Blueprint('mailTemplate', __name__)

from src.mailTemplate import routes