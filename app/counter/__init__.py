from flask import Blueprint

counter= Blueprint("counter",__name__, url_prefix="/api")

from .resources import *
