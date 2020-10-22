
def create_app(configfile):
    
    from flask import Flask
    app = Flask(__name__)
    app.config.from_pyfile(configfile)

    from .models import User,Client,Limits,UserTriesPerIdClient
    from .counter import counter
    from .api import api_v1
    
    app.register_blueprint(counter)
    app.register_blueprint(api_v1)
    from .ext import db,migrate,api
    db.init_app(app)
    migrate.init_app(app,db)
    api.init_app(app,api_v1)
    
    return app