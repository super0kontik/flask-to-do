from flask import Blueprint, render_template
from . import db
from .models import User, Task
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', user=current_user, tasks = tasks)