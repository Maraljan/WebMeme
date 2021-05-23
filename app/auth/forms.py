from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from wtforms import StringField, PasswordField


from app.models.auth import User


class LoginForm(FlaskForm):
    email_login = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password_login = PasswordField('Password', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[
        DataRequired(),
        Length(1, 64),
        Regexp(
            '^[A-Za-z][A-Za-z0-9_.]*$', 0,
            'Usernames must have only letters, numbers, dots or underscores'
        )
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('repeat_password', message='Password must match.'),
    ])
    repeat_password = PasswordField('Confirm password', validators=[DataRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
