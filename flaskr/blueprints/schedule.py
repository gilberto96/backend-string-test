import functools
from ..models.task import Task
from ..models.user import User
from ..models.responses import ApiResponse
from flask_jwt import jwt_required, current_identity

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

bp = Blueprint('schedule', __name__, url_prefix='/schedule')

@bp.route('/tasks', methods=['POST'])
@jwt_required()
def register():
    json = request.get_json(force = True)

    if json.get('title') is None or len(json["title"]) == 0:
        return jsonify(ApiResponse(0, False, 'Should specify a title for the task').toJson()), 400
    if json.get('start_date') is None or len(json["start_date"]) == 0:
        return jsonify(ApiResponse(0, False, 'Should specify a start date for the task').toJson()), 400
    if json.get('due_date') is None or len(json["due_date"]) == 0:
        return jsonify(ApiResponse(0, False, 'Should specify a due date for the task').toJson()), 400

    task = Task(
        title = json['title'], 
        description = json["description"],
        start_date = json["start_date"],
        due_date = json["due_date"],
        priority = json["priority"],
        assignee_user_id = current_identity.id
    )

    task = task.save()
    
    return jsonify(ApiResponse(task.id, True, "Task created").toJson())


@bp.route('/tasks/<id>', methods=['GET'])
@jwt_required()
def get(id):
    task = Task.get_single(id, current_identity.id)

    if task is None:
        return jsonify(ApiResponse(0, False, 'Task not found').toJson()), 404
    else:
        return jsonify(task.to_dict())


@bp.route('/tasks', methods=['GET'])
@jwt_required()
def list():
    user_id = current_identity.id
    user = User.get_by_id(user_id)

    if len(user.tasks) == 0:
        return jsonify([])
    else:
        return jsonify([ task.to_dict() for task in user.tasks ])

        
@bp.route('/tasks', methods=['PUT'])
@jwt_required()
def update():
    json = request.get_json(force=True)

    if json.get('id') is None:
            return jsonify(ApiResponse(0, False, "Must provide an task id").toJson()), 400

    task = Task.get_single(json["id"], current_identity.id)
    if task is None:
        return jsonify(ApiResponse(0, False, "The task does not exist").toJson()), 404

    # user = User.get_by_id(json["assignee_user_id"])
    # if user is None:
    #     return jsonify(ApiResponse(None, False, 'Assignee user not found').toJson()), 404

    task.title = json['title']
    task.description = json['description']
    task.start_date = json['start_date']
    task.due_date = json['due_date']
    task.priority = json['priority']
    task = task.save()

    return jsonify(ApiResponse(task.id, True, "Task updated").toJson())

      
@bp.route('/tasks/<id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    if not(id.isdigit()):
        return jsonify(ApiResponse(0, False, "Must provide an valid task id").toJson()), 400

    task = Task.get_single(id, current_identity.id)

    if task is None:
        return jsonify(ApiResponse(0, False, "The task does not exist").toJson()), 404

    return jsonify(ApiResponse(task.id, task.delete(), "Task removed").toJson())