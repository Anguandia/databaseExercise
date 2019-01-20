import os
from flask import Flask
from config.config import app_config
from app.db import Db

db_name='twice'


def create_app(config_name):
    from . import views
    app = Flask(__name__, instance_relative_config=True)
    #app.config.from_pyfile('config.py')
    app.config.from_object(app_config[config_name])
    app.db = Db(db_name)

    return app


#app = create_app(config_name=os.getenv('FLASK_ENV'))
