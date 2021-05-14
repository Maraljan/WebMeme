from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import ConfigName, configs

db = SQLAlchemy()


def create_app(config_name: ConfigName = ConfigName.DEFAULT) -> Flask:
    app = Flask(__name__)
    app.config.from_object(configs[config_name])

    db.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
