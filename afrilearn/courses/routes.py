from flask import render_template, request
from flask_login import login_required

from afrilearn.courses import courses
from afrilearn.models import LevelBlob, SubjectContainer
from .utils import get_pdf_url_with_blob_sas_token


@courses.route('/courses')
@login_required
def courses_func():
    return render_template('courses/user_courses.html', title='Courses')


@courses.route('/courses/primary-school')
@login_required
def primary_school():
    page = request.args.get('page', default=1, type=int)
    _courses = SubjectContainer.query.paginate(per_page=4, page=page)
    return render_template('courses/primary.html', courses=_courses, title='Primary School Material')


@courses.route('/courses/primary-school/<int:container>')
@login_required
def topic_subject(container):
    page = request.args.get('page', default=1, type=int)
    subjects_class = LevelBlob.query.filter_by(subject_id=container).paginate(per_page=4, page=page)
    container_name = SubjectContainer.query.filter_by(id=container).first().container
    return render_template("courses/subject.html", all_level_class=subjects_class, container_name=container_name, title="Papers", container=container)


@courses.route("/courses/primary-school/<container_name>/<blob_name>")
@login_required
def revision(container_name, blob_name):
    pdf_url_with_sas_token = get_pdf_url_with_blob_sas_token(container_name=container_name, blob_name=LevelBlob.query.get(blob_name).blob_name)
    return render_template(template_name_or_list="courses/paper.html", pdf_url_with_sas_token=pdf_url_with_sas_token, title='Revision')
