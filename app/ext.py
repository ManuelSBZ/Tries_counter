from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import redis
db = SQLAlchemy()
migrate = Migrate()
redis_connection = redis.Redis()