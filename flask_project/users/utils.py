import os
from secrets import token_hex

from PIL import Image
from flask import current_app, url_for
from flask_mail import Message

from flask_project import mail


def save_avatar(form_avatar):
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(form_avatar.filename)
    avatar_fn = random_hex + f_ext
    avatar_path = os.path.join(current_app.root_path,
                               'static/profile_avatar', avatar_fn)

    output_size = (150, 150)
    i = Image.open(form_avatar)
    i.thumbnail(output_size)
    i.save(avatar_path)

    return avatar_fn


def save_image(form_image):
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    avatar_fn = random_hex + f_ext
    avatar_path = os.path.join(current_app.root_path,
                               'static/img/posts_image', avatar_fn)

    output_size = (440, 220)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(avatar_path)

    return avatar_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request.',
                  sender='igeekshop@inbox.ru',
                  recipients=[user.email])
    msg.body = f'''
        To reset your password, click on the following link: 
        {url_for('users.reset_token', token=token, _external=True)} 
        If you didn't make this request then just ignore this email and there will be no changes.
        '''
    mail.send(msg)
