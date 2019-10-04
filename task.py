from .models import User, Task
from . import db
from flask_login import login_required, current_user
from flask import Blueprint, request, redirect, url_for

task = Blueprint('task', __name__)


@task.route('/task', methods=['POST'])
@login_required
def add_task():
    uid = request.form.get('uid')
    if not uid:
        uid = current_user.id
    task_content = request.form.get('content')
    user = User.query.filter_by(id=uid).first()
    if not user:
        return 'User does not exists'

    task = Task(content=task_content)
    user.tasks.append(task)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('main.profile'))


@task.route('/task', methods=['PATCH'])
@login_required
def update_task():
    json_content = request.get_json()
    print(json_content)
    task_id = json_content['taskId']
    new_content = json_content['content']
    task = Task.query.filter_by(id=int(task_id)).first()
    if not task:
        return 'Task does not exist'

    task.content = new_content
    db.session.commit()
    return task.content


@task.route('/task/<id>', methods=['PUT'])
@login_required
def check_task(id):
    task = Task.query.filter_by(id=int(id)).first()
    if not task:
        return 'Task does not exist'

    task.completed = 1 if task.completed == 0 else 0
    db.session.commit()
    return task.completed


@task.route('/task/<id>', methods=['DELETE'])
@login_required
def remove_task(id):
    task = Task.query.filter_by(id=int(id)).first()
    if not task:
        return 'Task does not exist'

    db.session.delete(task)
    db.session.commit()
    return 'ok'