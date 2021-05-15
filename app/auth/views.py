from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user

from . import auth
from app import db
from app.auth.forms import LoginForm, RegistrationForm
from app.models.auth import User
from app.common.alerts import Alert


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if next_page is None or not next_page.startswith('/'):
                next_page = url_for('main.index')
            return redirect(next_page)
        flash('Invalid email or password.', Alert.DANGER)
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', Alert.DARK)
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data.lower(),
            username=form.username.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration is successful. Now you can try to login', Alert.SUCCESS)
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)
