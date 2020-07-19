from flask import Blueprint

courses = Blueprint('courses', __name__)

from afrilearn.courses import routes
