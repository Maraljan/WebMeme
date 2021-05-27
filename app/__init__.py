from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import ConfigName, configs

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.authorization'


def create_app(config_name: ConfigName = ConfigName.DEFAULT) -> Flask:
    app = Flask(__name__)
    app.config.from_object(configs[config_name])

    db.init_app(app)

    login_manager.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
