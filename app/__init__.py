import os
from flask_api import FlaskAPI
from instance.config import app_config


def create_app(config_name):
    from . import views
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    app.config.from_object(app_config[config_name])

    return app


#app = create_app(config_name=os.getenv('FLASK_ENV'))
