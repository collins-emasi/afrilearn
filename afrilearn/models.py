import flask_whooshalchemy as fwa
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from afrilearn import app
from afrilearn import db, login_manager
from config import blob_service_client


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class SubjectContainer(db.Model):
    __searchable__ = ['container']
    __bind_key__ = 'courses'
    __tablename__ = 'Subject'
    # This is the container eg english, kiswahili
    id = db.Column(db.Integer, primary_key=True)
    container = db.Column(db.String(100), nullable=False)
    level = db.relationship('LevelBlob', backref='subject', lazy=True)

    @staticmethod
    def get_class_levels(container):
        # Get the container
        container_client = blob_service_client.get_container_client(container)
        # List the blobs in the container
        classes = container_client.list_blobs()
        return classes

    def __repr__(self):
        return f"{self.container}"


class LevelBlob(db.Model):
    __searchable__ = ['blob_name']
    __bind_key__ = 'courses'
    __tablename__ = 'Level'
    # This is the blob eg english class1 pdf, kiswahili class 8 pdf
    id = db.Column(db.Integer, primary_key=True)
    blob_name = db.Column(db.String(100), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('Subject.id'), nullable=False)

    def __repr__(self):
        return f"{self.blob_name}"


fwa.whoosh_index(app=app, model=SubjectContainer)
fwa.whoosh_index(app=app, model=LevelBlob)