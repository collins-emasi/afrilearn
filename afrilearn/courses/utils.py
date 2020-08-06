from datetime import datetime, timedelta

from azure.storage.blob import generate_container_sas, ContainerSasPermissions, generate_blob_sas, BlobSasPermissions

from afrilearn.models import LevelBlob, SubjectContainer
from afrilearn import db
from config import ACCOUNT_NAME, ACCOUNT_KEY


def add_course_to_db(course):
    s = SubjectContainer(container=course)
    db.session.add(s)
    db.session.commit()
    for blob in s.get_class_levels(container=course):
        b = LevelBlob(blob_name=blob.name, subject_id=s.id)
        db.session.add(b)
    db.session.commit()


def get_pdf_url_with_container_sas_token(blob_name, container_name):
    container_sas_token = generate_container_sas(
        account_name=ACCOUNT_NAME,
        container_name=container_name,
        account_key=ACCOUNT_KEY,
        permission=ContainerSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    blob_url_with_container_sas_token = f"https://{ACCOUNT_NAME}.blob.core.windows.net/{container_name}/{blob_name}?{container_sas_token}"
    return blob_url_with_container_sas_token


def get_pdf_url_with_blob_sas_token(blob_name, container_name):
    blob_sas_token = generate_blob_sas(
        account_name=ACCOUNT_NAME,
        container_name=container_name,
        blob_name=blob_name,
        account_key=ACCOUNT_KEY,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    blob_url_with_blob_sas_token = f"https://{ACCOUNT_NAME}.blob.core.windows.net/{container_name}/{blob_name}?{blob_sas_token}"
    return blob_url_with_blob_sas_token

