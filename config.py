import os
from urllib.parse import quote_plus
from azure.storage.blob import BlobServiceClient

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
AFRILEARN_MAIL_SUBJECT_PREFIX = '[AfriLearn]'
AFRILEARN_MAIL_SENDER = 'AfriLearn Admin <noreply@afrilearn.com>'
WHOOSH_BASE = 'whoosh'
SQLALCHEMY_TRACK_MODIFICATIONS = True
ACCOUNT_KEY = os.environ.get('ACCOUNT_KEY')
ACCOUNT_NAME = 'reaiotblobs'
ODBC_CONNECTION_STRING = os.environ.get('ODBC_CONNECTION_STRING')
BLOB_CONNECTION_STRING = os.environ.get('BLOB_CONNECTION_STRING')
params = quote_plus(ODBC_CONNECTION_STRING)
blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "mssql+pyodbc:///?odbc_connect=%s" % params
SQLALCHEMY_BINDS = os.environ.get('DEV_BINDS') or {"courses": "sqlite:///courses.db"}