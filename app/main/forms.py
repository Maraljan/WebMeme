from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms import StringField, FileField, BooleanField

from app.models.meme import MemeTemplate


class TemplateForm(FlaskForm):
    img = FileField('Image', validators=[FileRequired()])
    title = StringField('Title', validators=[DataRequired(), Length(1, 64)])

    def validate_title(self, field: StringField):
        if MemeTemplate.query.filter_by(title=field.data, owner_id=current_user.pk).first():
            raise ValidationError('Title already used')


class MemeForm(FlaskForm):
    text_top = StringField('Text_top', validators=[DataRequired(), Length(1, 64)])
    text_bottom = StringField('Text_bottom', validators=[DataRequired(), Length(1, 64)])
    save_to_desktop = BooleanField()
