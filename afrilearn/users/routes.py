import json, secrets

import requests
from flask import redirect, url_for, render_template, flash, request
from flask_login import current_user, login_user, logout_user, login_required

from afrilearn import db, bcrypt
from afrilearn.models import User, UserModel
from afrilearn.users import users
from afrilearn.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from afrilearn.users.utils import save_pic, send_reset_email

endpoint = "https://reaiotbackend.azurewebsites.net"

headers = {
    'Authorization': 'password',
    'Content-Type': 'application/json',
}


def auth_user(payload):
    response = requests.post(url=endpoint + "/api/User/authenticateUser", data=json.dumps(payload), headers=headers)
    conn = db.engine.connect()
    result = conn.execute("SELECT * FROM AspNetUsers WHERE Email = '{}'".format(payload['email'])).first()
    return response, result


def create_user(payload):
    response = requests.post(url=endpoint + "/api/User/register", data=json.dumps(payload), headers=headers)
    return response


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        payload = {
            "id": secrets.token_hex(24),
            "userName": form.username.data,
            "email" : form.email.data,
            "passwordHash": form.password.data,
            "role": "customer",
        }
        response = create_user(payload)
        if response.ok:
            flash(message='Account created successfully. Please login', category='success')
            return redirect(url_for('users.login'))
    return render_template('users/register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        payload = {
            "email": form.email.data,
            "password": form.password.data,
        }
        response, result = auth_user(payload)
        if response.ok:
            user = UserModel(email=form.email.data)
            login_user(user=user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash("Log in successful", 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Check email or password', 'danger')
    return render_template('users/login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_pic(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated successfully', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('users/account.html', title='Account', image_file=image_file, form=form)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset password', 'info')
        return redirect('login')
    return render_template('users/reset_request.html', title='Reset Password', form=form)


@users.route("/resete_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token=token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(message='Password Reset Successful. Please log in', category='success')
        return redirect(url_for('users.login'))
    return render_template("users/reset_token.html", title="Reset Password", form=form)
