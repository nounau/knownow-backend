from flask import Blueprint

bp = Blueprint('mailTemplate', __name__)

from app.mailTemplate import routes