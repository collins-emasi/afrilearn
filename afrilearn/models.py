from datetime import datetime, timedelta

import flask_whooshalchemy as fwa
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from afrilearn import app, ma, ACCOUNT_NAME, ACCOUNT_KEY
from afrilearn import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    id_element = db.Column(db.String(120), unique=True, nullable=False)
    userName = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='customer')

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
        return f"User('{self.userName}', '{self.email}')"


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    id_element = ma.auto_field()
    userName = ma.auto_field()
    email = ma.auto_field()
    password = ma.auto_field()
    role = ma.auto_field()


class SubjectContainer(db.Model):
    __searchable__ = ['name', 'level', 'container']
    __bind_key__ = 'courses'
    __tablename__ = 'Subject'
    # This is the container eg english, kiswahili
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    container = db.Column(db.String(50), nullable=False)

    def get_pdf_url_with_blob_sas_token(self):
        blob_sas_token = generate_blob_sas(
            account_name=ACCOUNT_NAME,
            container_name=self.container,
            blob_name=self.name,
            account_key=ACCOUNT_KEY,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )
        blob_url_with_blob_sas_token = f"https://{ACCOUNT_NAME}.blob.core.windows.net/{self.container}/{self.name}?{blob_sas_token}"
        return blob_url_with_blob_sas_token

    def __repr__(self):
        return f"{self.name}"


fwa.whoosh_index(app=app, model=SubjectContainer)
