from afrilearn.models import LevelBlob, SubjectContainer
from afrilearn import db


def add_course_to_db(course):
    s = SubjectContainer(container=course)
    db.session.add(s)
    db.session.commit()
    for blob in s.get_class_levels(container=course):
        b = LevelBlob(blob_name=blob.name, subject_id=s.id)
        db.session.add(b)
    db.session.commit()
