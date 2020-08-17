from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from sqlalchemy import text
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from afrilearn.models import User
from afrilearn import db

conn = db.engine.connect()


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(2, 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = conn.execute(text("SELECT * FROM AspNetUsers WHERE UserName = '{}'".format(username))).fetchall()
        if user:
            raise ValidationError('That username is taken. Please choose another one')

    def validate_email(self, email):
        user = conn.execute(text("SELECT * FROM AspNetUsers WHERE Email = '{}'".format(email))).fetchall()
        if user:
            raise ValidationError('Email is taken. Please Choose another one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(2, 20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = conn.execute(text("SELECT * FROM AspNetUsers WHERE UserName = '{}'".format(username))).fetchall()
            if user:
                raise ValidationError('That username is taken. Please choose another one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = conn.execute(text("SELECT * FROM AspNetUsers WHERE Email = '{}'".format(email))).fetchall()
            if user:
                raise ValidationError('Email is taken. Please Choose another one')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField('Reset Password')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No account with that email. Please register')
