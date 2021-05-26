from flask import render_template, redirect, url_for, request
from flask_login import login_user, login_required, logout_user

from . import auth
from app import db
from app.auth.forms import LoginForm, RegistrationForm
from app.models.auth import User
from app.common.alerts import Alert, alert


@auth.route('/login', methods=['GET', 'POST'])
def authorization():
    login_form = LoginForm()
    register_form = RegistrationForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email_login.data.lower()).first()
        if user is not None and user.verify_password(login_form.password_login.data):
            login_user(user)
            next_page = request.args.get('next')
            if next_page is None or not next_page.startswith('/'):
                next_page = url_for('main.index')
            return redirect(next_page)
        alert('Invalid email or password.', Alert.DANGER)
    elif register_form.validate_on_submit():
        user = User(
            email=register_form.email.data.lower(),
            username=register_form.username.data,
            password=register_form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        alert('Registration is successful. Now you can try to login', Alert.SUCCESS)
        return redirect(url_for('auth.authorization'))

    return render_template('auth/authorization.html', login_form=login_form, register_form=register_form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    alert('You have been logged out.', Alert.DARK)
    return redirect(url_for('auth.authorization'))
