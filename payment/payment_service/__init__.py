from flask import Flask
from payment_service import views
from payment_service.database import *
# from flask.ext.mongoalchemy import MongoAlchemy
# from config import Config

# db = MongoAlchemy()

def getAppContext():
    app = Flask(__name__)
    app.config.from_object(__name__)
    # app.config.from_object(Config)

    # db.init_app(app)
    db = Database()
    
    app.register_blueprint(views.payment)

    return app