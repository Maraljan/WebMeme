from enum import Enum

from flask import flash


class Alert(str, Enum):

    PRIMARY = "alert-primary"
    SECONDARY = "alert-secondary"
    SUCCESS = "alert-success"
    DANGER = "alert-danger"
    WARNING = "alert-warning"
    INFO = "alert-info"
    LIGHT = "alert-light"
    DARK = "alert-dark"


def alert(message: str, category: Alert = Alert.DANGER):
    flash(message, category)
