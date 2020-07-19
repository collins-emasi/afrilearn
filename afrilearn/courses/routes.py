from flask import render_template, request
from flask_login import login_required

from afrilearn.models import LevelBlob, SubjectContainer
from afrilearn.courses import courses


@courses.route("/courses/revision/<int:container_id>/<blob_name>")
@login_required
def revision(container_id, blob_name):
    pdf_url_with_sas_token = LevelBlob.get_pdf_url_with_blob_sas_token(blob_name,
                                                                       SubjectContainer.query.get(
                                                                           container_id).container)
    return render_template('revision_paper.html', pdf_url_with_sas_token=pdf_url_with_sas_token, blob_name=blob_name, title="Revision")


@courses.route('/courses/primary_school')
@login_required
def primary_school():
    page = request.args.get('page', default=1, type=int)
    _courses = SubjectContainer.query.paginate(per_page=4, page=page)
    return render_template('courses/primary.html', courses=_courses, title='Primary School Material')


@courses.route('/courses')
@login_required
def courses_func():
    return render_template('courses/user_courses.html', title='Courses')


@courses.route('/courses/<int:container>')
@login_required
def topic_subject(container):
    page = request.args.get('page', default=1, type=int)
    subjects_class = LevelBlob.query.filter_by(subject_id=container).paginate(per_page=4, page=page)
    return render_template("courses/subject.html", all_level_class=subjects_class, container=container, title="Papers")
