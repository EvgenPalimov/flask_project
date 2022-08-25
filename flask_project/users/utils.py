import os
from secrets import token_hex

from PIL import Image
from flask import current_app


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

