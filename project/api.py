from flask import Blueprint, jsonify

todo_blueprint = Blueprint('todo', __name__)

@todo_blueprint.route('/todo/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })