import os
import secrets

from PIL import Image
from flask import url_for
from flask_mail import Message

from afrilearn import mail, app


def save_pic(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_pic)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(app.config['AFRILEARN_MAIL_SUBJECT_PREFIX'] + 'Password Reset Request', sender='noreply@afrilearn.com', recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}


If you did not request this email, simply ignore this mail.
    """
    mail.send(msg)
