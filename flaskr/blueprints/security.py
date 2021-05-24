import functools
from re import I
from ..models.user import User
from ..models.responses import ApiResponse

from flask import (
    Blueprint, flash, g, json, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import generate_password_hash

bp = Blueprint('security', __name__, url_prefix='/security')

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
    user.password = None
    if user is None:
        return jsonify(ApiResponse(0, False, 'User not found').toJson()), 404
    else:
        return jsonify(user.to_dict())
        
@bp.route('/users/', methods=['GET'])
def list():
    users = [ {
        "fullname": user.fullname,
        "id": user.id,
        "email": user.email,
        "photo": user.photo,
        "created_at": user.created_at
    } for user in User.get_all() ] 

    return jsonify(users)
            
@bp.route('/users', methods=['PUT'])
def update():
    json = request.get_json(force=True)

    if json.get('id') is None:
        return jsonify(ApiResponse(0, False, "Must provide an user id").toJson()), 400

    user = User.get_by_id(id=json['id'])

    if user is None:
        return jsonify(ApiResponse(0, False, "The user does not exist").toJson()), 404

    user.email = json['email']
    user.fullname = json['fullname']
    user.photo = json['photo']
    user = user.save()

    return jsonify(ApiResponse(user.id, True, "User updated").toJson())
       
@bp.route('/users/<id>', methods=['DELETE'])
def delete(id):
    if not(id.isdigit()):
        return jsonify(ApiResponse(0, False, "Must provide an valid user id").toJson()), 400

    user = User.get_by_id(int(id))
    
    if user is None:
        return jsonify(ApiResponse(0, False, "The user does not exist").toJson()), 404
    
    if len(user.tasks) > 0:
        return jsonify(ApiResponse(0, False, "The user have asossiated tasks").toJson()), 400

    user.delete()

    return jsonify(ApiResponse(user.id, True,"User removed").toJson())
