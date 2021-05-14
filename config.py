import os
from enum import Enum
from pathlib import Path

# absolute path to project dir
BASEDIR = Path(__file__).parent


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        f"sqlite:///{BASEDIR.joinpath('data-dev.sqlite')}"


class ConfigName(str, Enum):
    """
    Constants for config names.
    """
    DEVELOPMENT = 'development'
    DEFAULT = 'default'


configs = {
    ConfigName.DEVELOPMENT: DevelopmentConfig,
    ConfigName.DEFAULT: DevelopmentConfig,
}

