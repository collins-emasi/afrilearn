# import os
# from urllib.parse import quote_plus
# from azure.storage.blob import BlobServiceClient
#
#
# basedir = os.path.abspath(os.path.dirname(__file__))
#
# account_key = "LjPUMFKQLs5aosGxEHddgDdt1sdCAqFcFhaP3KuKVcsNCIH2vpNcsx5cwKu98RUgVwgbQeLKbGsZT+sObvqQjA=="
# blob_conn_str = "DefaultEndpointsProtocol=https;AccountName=reaiotblobs;AccountKey=LjPUMFKQLs5aosGxEHddgDdt1sdCAqFcFhaP3KuKVcsNCIH2vpNcsx5cwKu98RUgVwgbQeLKbGsZT+sObvqQjA==;EndpointSuffix=core.windows.net"
#
# SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
# MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
# MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
# MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
# MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
# MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
# AFRILEARN_MAIL_SUBJECT_PREFIX = '[AfriLearn]'
# AFRILEARN_MAIL_SENDER = 'AfriLearn Admin <noreply@afrilearn.com>'
# WHOOSH_BASE = 'whoosh'
# SQLALCHEMY_TRACK_MODIFICATIONS = True
# ACCOUNT_KEY = os.environ.get('ACCOUNT_KEY', account_key)
# ACCOUNT_NAME = 'reaiotblobs'
# # ODBC_CONNECTION_STRING = os.environ.get('ODBC_CONNECTION_STRING')
# ODBC_CONNECTION_STRING="Driver={ODBC Driver 17 for SQL Server};Server=tcp:reaiot.database.windows.net,1433;Database=ReaiotDb;Uid=reaiot;Pwd={2288Shiks.};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
# BLOB_CONNECTION_STRING = os.environ.get('BLOB_CONNECTION_STRING', blob_conn_str)
# params = quote_plus(ODBC_CONNECTION_STRING)
# blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "mssql+pyodbc:///?odbc_connect=%s" % params
# SQLALCHEMY_BINDS = os.environ.get('DEV_BINDS') or {"courses": "sqlite:///courses.db"}
