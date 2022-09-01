from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_project import db, bcrypt
from flask_project.models import User, Post
from flask_project.users.forms import (RegistrationForm, LoginForm,
                                       UpdateAccountForm, RequestResetForm,
                                       ResetPasswordForm)
from flask_project.users.utils import save_avatar, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.avatar.data:
            avatar = save_avatar(form.avatar.data)
        else:
            avatar = 'default.png'
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password,
                    image_file=avatar)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! Now you can log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.allpost'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else \
                redirect(url_for('posts.allpost'))
        else:
            flash('Login failed. Please check your email and password.',
                  'attention')
    return render_template('login.html', title='Authentication', form=form)


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.avatar.data:
            avatar_file = save_avatar(form.avatar.data)
            current_user.image_file = avatar_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        page = request.args.get('page', 1, type=int)
        user = User.query.filter_by(username=form.username.data).first_or_404()
        posts = Post.query.filter_by(author=user) \
            .order_by(Post.date_posted.desc()) \
            .paginate(page=page, per_page=5)
        if user.image_file:
            image_file = url_for('static', filename='profile_avatar/'
                                                    + current_user.image_file)
        else:
            image_file = url_for('static',
                                 filename='profile_avatar/default.png')

        return render_template('account.html', title='Account',
                               image_file=image_file, form=form,
                               posts=posts, user=user)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('posts.allpost'))

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('posts.allpost'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with '
              'instructions on how to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',
                           title='Reset password',
                           form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('posts.allpost'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('The link is outdated, try resetting the password again.',
              'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)\
            .decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been successfully updated.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',
                           title='Reset password',
                           form=form)