from flask import render_template, Blueprint
from flask_project.models import User

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html', title='Index')


@main.route('/about')
def about():
    return render_template('about.html', title='About')


@main.route('/post')
def post():
    return render_template('post.html', title='Post')


@main.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')
