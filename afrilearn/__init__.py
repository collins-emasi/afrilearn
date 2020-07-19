from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import *
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['WHOOSH_BASE'] = WHOOSH_BASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS
app.config['AFRILEARN_MAIL_SUBJECT_PREFIX'] = AFRILEARN_MAIL_SUBJECT_PREFIX

db = SQLAlchemy(app)
login_manager = LoginManager(app)
mail = Mail(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)


db.init_app(app)
login_manager.init_app(app)
mail.init_app(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
login_manager.session_protection = 'strong'
csrf.init_app(app)
bcrypt.init_app(app)

from afrilearn.main import main as main_blueprint
from afrilearn.users import users as users_blueprint
from afrilearn.courses import courses as courses_blueprint

app.register_blueprint(main_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(courses_blueprint)

subjects = [
    'english',
    'mathematics',
    'kiswahili',
    'science',
    'religious-education',
    'social-studies'
]
