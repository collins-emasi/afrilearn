from flask import render_template
from afrilearn.main import main


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html', title='page not found'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html', title='internal server error'), 500
