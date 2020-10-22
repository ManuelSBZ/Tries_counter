from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_rest_jsonapi import Api

db = SQLAlchemy()
migrate = Migrate()
api =  Api()