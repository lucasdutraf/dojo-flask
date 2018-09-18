from flask import Blueprint, jsonify, request

from sqlalchemy import exc

from project.api.models import Task
from project import db

tasks_blueprint = Blueprint('tasks', __name__)

@tasks_blueprint.route('/api/tasks', methods=['GET'])
def get_all_tasks():
    response = {
        'status': 'success',
        'data': {
            'tasks': [task.to_json() for task in Task.query.all()]
        }
    }
    return jsonify(response), 200

@tasks_blueprint.route('/api/tasks', methods=['POST'])
def add_task():
    post_data = request.get_json()

    error_response = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }

    if not post_data:
        return jsonify(error_response), 400

    title = post_data.get('title')
    description = post_data.get('description')

    try:
        db.session.add(Task(title, description))
        db.session.commit()

        response = {
            'status': 'success',
            'data': {
                'message': f'Task {title} - {description} was created!'
            }
        }

        return jsonify(response), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(error_response), 400


@tasks_blueprint.route('/api/tasks/<task_id>', methods=['GET'])
def get_single_task(task_id):
    error_response = {
        'status': 'fail',
        'message': 'Task not found'
    }
    try:
        task = Task.query.filter_by(id=int(task_id)).first()

        if not task:
            return jsonify(error_response), 404

        response = {
            'status': 'success',
            'data': task.to_json()
        }
    except ValueError:
        return jsonify(error_response), 404

    return jsonify(response), 200

@tasks_blueprint.route('/api/tasks/<task_id>', methods=['PATCH'])
def update_task_status(task_id):
    post_data = request.get_json()

    done = post_data.get('done')

    task = Task.query.filter_by(id=int(task_id)).first()
    task.done = done
    db.session.commit()

    if task.done:
        response = {
            'status': 'success',
            'data': {
                'task_status': 'Task completed!'
            }
        }
    else:
        response = {
            'status': 'success',
            'data': {
                'task_status': 'Task not complete!'
            }
        }

    return jsonify(response), 200

@tasks_blueprint.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.filter_by(id=int(task_id)).first()
    db.session.delete(task)
    db.session.commit()

    response = {
        'status': 'success',
        'data': {
            'message': 'Task deleted!'
        }
    }

    return jsonify(response), 200
    
