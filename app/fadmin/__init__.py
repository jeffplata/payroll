from flask import Blueprint

bp = Blueprint('fadmin', __name__)

from app.fadmin import controller
