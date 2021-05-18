from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms import StringField, FileField

from app.models.meme import MemeTemplate


class TemplateForm(FlaskForm):
    img = FileField('Image', validators=[FileRequired()])
    title = StringField('Title', validators=[DataRequired(), Length(1, 64)])

    def validate_title(self, field: StringField):
        if MemeTemplate.query.filter_by(title=field.data).first():
            raise ValidationError('Title already used')
