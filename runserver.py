import os

from flask_migrate import Migrate

from app import create_app, db
from app.models.auth import User
from config import ConfigName

app = create_app(os.getenv('FLASK_CONFIG') or ConfigName.DEFAULT)
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)


if __name__ == '__main__':
    app.run()
