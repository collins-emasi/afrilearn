from flask import render_template, request, flash
from flask_login import current_user
from sqlalchemy import func, distinct

from afrilearn import db
from afrilearn.main.forms import SearchForm
from afrilearn.models import SubjectContainer
from afrilearn.main import main


@main.route('/')
@main.route('/home')
def home():
    form = SearchForm()
    page = request.args.get('page', default=1, type=int)
    _courses = db.session.query(distinct(SubjectContainer.level)).paginate(per_page=2, page=page)
    # _courses = SubjectContainer.query(distinct(SubjectContainer.subject)).paginate(per_page=2, page=page)
    return render_template('main/home.html', current_user=current_user, _courses=_courses, form=form, bool_val=True)


@main.route('/search')
def search():
    form = SearchForm()
    page = request.args.get('page', default=1, type=int)
    results = SubjectContainer.query.whoosh_search(request.args.get('query')).paginate(per_page=2, page=page)
    if not results.items:
        flash(f"Sorry No courses found for {request.args.get('query')}.", 'danger')
    return render_template('main/home.html', _courses=results, form=form, bool_val=False, whoosh=True)


@main.route('/about')
def about():
    return render_template('main/about.html', title='About')
