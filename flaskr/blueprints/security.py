import functools
from re import I
from ..models.user import User
from ..models.responses import ApiResponse
from flask_jwt import jwt_required, current_identity

from flask import (
    Blueprint, flash, g, json, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/security')

@bp.route('/users/', methods=['POST'])
def register():
    json = request.get_json(force = True)

    if json.get('email') is None or json.get('password') is None:
        return jsonify(ApiResponse(0, False, 'Username and password required').toJson()), 400

    user = User(
        email = json['email'], 
        password = generate_password_hash(json["password"]),
        fullname = json["fullname"],
        photo = json["photo"]
    )

    user = user.save()
    
    return jsonify(ApiResponse(user.id, True, "User created").toJson())


@bp.route('/users/<id>', methods=['GET'])
def get(id):
    user = User.get_by_id(id)

    if user is None:
        return jsonify(ApiResponse(0, False, 'User not found').toJson()), 404
    else:
        return jsonify(user.to_dict())
        
@bp.route('/users/', methods=['GET'])
def list():
    users = [ user.to_dict() for user in User.get_all() ] 

    return jsonify(users)
            
@bp.route('/users', methods=['PUT'])
def update():
    json = request.get_json(force=True)

    if json.get('id') is None:
        return jsonify(ApiResponse(None, False, "Must provide an user id").toJson()), 400

    user = User.query.filter_by(id=json['id']).first()

    if user is None:
        return jsonify(ApiResponse(None, False, "The user does not exist").toJson()), 404

    user.email = json['email']
    user.fullname = json['fullname']
    user.photo = json['photo']
    user = user.save()

    return jsonify(ApiResponse(user.id, True, "Task updated").toJson())
       
@bp.route('/users/<id>', methods=['DELETE'])
def delete(id):
    if not(id.isdigit()):
        return jsonify(ApiResponse(None, False, "Must provide an valid user id").toJson()), 400

    user = User.query.filter_by(id=int(id)).first()
    
    if user is None:
        return jsonify(ApiResponse(None, False, "The user does not exist").toJson()), 404
    
    if len(user.tasks) > 0:
        return jsonify(ApiResponse(None, False, "The user have asossiated tasks").toJson()), 400

    user.delete()

    return jsonify(ApiResponse(None, True,"User removed").toJson())
