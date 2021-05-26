from pathlib import Path

from flask import url_for
from sqlalchemy.orm import relationship

from app import db
from config import IMAGES_DIR


class Common:
    image_path = db.Column(db.String(128))

    def image_url(self) -> str:
        path = Path(IMAGES_DIR.name).joinpath(self.image_path)
        return url_for('static', filename=str(path).replace('\\', '/'))


class MemeTemplate(db.Model, Common):
    __tablename__ = 'MemeTemplate'
    pk = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.pk'))
    memes = relationship('Meme', backref='template')
    __table_args__ = (db.UniqueConstraint('title', 'owner_id', name='user_uniq_template'), )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f'<MemeTemplate {self.title}>'


db.Index('user_uniq_template', MemeTemplate.title, MemeTemplate.owner_id, unique=True)


class Meme(db.Model, Common):
    __tablename__ = 'Meme'
    pk = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.pk'))
    template_id = db.Column(db.Integer, db.ForeignKey('MemeTemplate.pk'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
