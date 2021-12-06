from flask import Blueprint

counter= Blueprint("counter",__name__)

from .resources import *
