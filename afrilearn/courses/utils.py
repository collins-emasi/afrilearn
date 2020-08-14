from datetime import datetime, timedelta

from azure.storage.blob import generate_container_sas, ContainerSasPermissions, generate_blob_sas, BlobSasPermissions

from afrilearn.models import SubjectContainer
from afrilearn import db
from config import ACCOUNT_NAME, ACCOUNT_KEY, blob_service_client


def add_course_to_db(name, level, subject, container):
    s = SubjectContainer(name=name, subject=subject, level=level, container=container)
    db.session.add(s)
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


def get_primary_subjects(container):
    primary = []
    container_client = blob_service_client.get_container_client(container)
    classes = container_client.list_blobs()
    for i in classes:
        if i.name.split('/')[0] == 'primary':
            primary.append(i)
    return primary


def get_secondary_subjects(container):
    secondary = []
    container_client = blob_service_client.get_container_client(container)
    classes = container_client.list_blobs()
    for i in classes:
        if i.name.split('/')[0] == 'secondary':
            secondary.append(i)
    return secondary


subjects = [
    "agriculture",
    "biology",
    "business-studies",
    "chemistry",
    "computer-studies",
    "english",
    "geography",
    "history",
    "home-science",
    "kiswahili",
    "mathematics",
    "physics",
    "religious-education",
    "set-books",
]

container_name = 'freelearn'


def fill_db():
    primary = get_primary_subjects(container_name)
    secondary = get_secondary_subjects(container_name)

    for p in primary:
        add_course_to_db(name=p.name, level='primary', subject=p.name.split('/')[1], container=container_name)

    for s in secondary:
        add_course_to_db(name=s.name, level='secondary', subject=s.name.split('/')[1], container=container_name)


def create_db():
    db.create_all(bind='courses')