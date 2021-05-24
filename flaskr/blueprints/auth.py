from datetime import timedelta, timezone
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from flaskr.models.tokenblocklist import TokenBlockList
from ..models.user import User
from flask_jwt_extended import create_access_token
from ..models.responses import ApiResponse
from flask_jwt_extended import jwt_required, get_jwt
from ..database import db

from flask import (
    Blueprint, flash, g, json, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import generate_password_hash

ACCESS_EXPIRES = timedelta(hours=1)


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.authenticate(email,password)
    if user is None:
        return jsonify(ApiResponse(0,False,"Invalid credentials").toJson()), 401
    access_token = create_access_token(identity=user.to_dict())
    return jsonify(access_token=access_token)

@bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlockList(jti=jti, created_at=now))
    db.session.commit()

    return jsonify(ApiResponse(0, True, "User logged out").toJson())