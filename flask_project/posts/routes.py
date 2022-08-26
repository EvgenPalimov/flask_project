import datetime

from flask import Blueprint, request, render_template, flash, abort, redirect, \
    url_for
from flask_login import login_required, current_user

from flask_project import db
from flask_project.models import Post
from flask_project.posts.forms import PostForm
from flask_project.users.utils import save_image

posts = Blueprint('posts', __name__)


@posts.route('/')
def allpost():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()). \
        paginate(page=page, per_page=4)
    return render_template('index.html', posts=posts, datetime=datetime)


@posts.route('/posts/user/<int:user_id>')
@login_required
def user_posts(user_id):
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.user_id == user_id). \
        order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('user_posts.html', posts=posts, datetime=datetime)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.image_file.data:
            image_file = save_image(form.image_file.data)
            post = Post(title=form.title.data, content=form.content.data,
                        user_id=current_user.id, image_file=image_file)
            db.session.add(post)
        else:
            post = Post(title=form.title.data, content=form.content.data,
                        user_id=current_user.id, image_file='default.jpg')
            db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
    return render_template('create_post.html', title='New post', form=form,
                           legend='New post')


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post,
                           datetime=datetime)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.image_file.data:
            image_file = save_image(form.image_file.data)
            post.image_file = image_file
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        if post.image_file:
            image_file = url_for('static', filename='img/posts_image/'
                                                    + post.image_file)
        else:
            image_file = url_for('static',
                                 filename='img/posts_image/default.png')

        return render_template('create_post.html', title='Update of post.',
                               form=form, legend='Update of post.',
                               image_file=image_file)


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been delete!', 'success')
    return redirect(url_for('posts.allpost'))
