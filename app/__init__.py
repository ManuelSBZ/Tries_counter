
def create_app(configfile):
    
    from flask import Flask
    app = Flask(__name__)
    app.config.from_pyfile(configfile)

    from .models import Limits, UserTries
    from .counter import counter
    
    app.register_blueprint(counter)
    
    from .ext import db,migrate
    db.init_app(app)
    migrate.init_app(app,db)
    
    return app