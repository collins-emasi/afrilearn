from flask import render_template, request
from flask_login import login_required
from sqlalchemy import distinct

from afrilearn.courses import courses
from afrilearn.models import SubjectContainer
from .. import db

container = 'freelearn'


@courses.route('/courses')
# @login_required
def courses_func():
    return render_template('courses/user_courses.html', title='Courses')


@courses.route('/courses/<school>')
# @login_required
def what_school(school):
    page = request.args.get('page', default=1, type=int)
    _courses = db.session.query(distinct(SubjectContainer.subject)).filter_by(level=school).paginate(per_page=4, page=page)
    # _courses = SubjectContainer.query.filter_by(level=school).paginate(per_page=4, page=page)
    if school == 'primary':
        title = 'Primary School Material'
    else:
        title = 'Secondary School Material'
    return render_template('courses/school.html', courses=_courses, title=title, school=school)


@courses.route('/courses/<school>/<subject>')
def school_subject(school, subject):
    page = request.args.get('page', default=1, type=int)
    all_level_class = SubjectContainer.query.filter_by(subject=subject).paginate(per_page=4, page=page)
    return render_template('courses/subject.html', all_level_class=all_level_class, title='{} School {}'.format(school.title(), subject))


@courses.route('/courses/revision-paper/lkkGHWddTZQKIHfjrdjjkdoeoFGDDldejjlajdiwkao0098ujeWERvf345uu/<string:blob_name>')
def revision_pdf(blob_name):
    blob = SubjectContainer.query.get(blob_name)
    pdf_url_with_sas_token = blob.get_pdf_url_with_blob_sas_token()
    return render_template("courses/paper.html", pdf_url_with_sas_token=pdf_url_with_sas_token, title='Revision')
