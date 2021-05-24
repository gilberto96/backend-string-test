import os
from flask import Flask, url_for, jsonify
from sqlalchemy_utils import create_database, database_exists
from .config import *
from flask_jwt_extended import JWTManager

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='j/6Ds!3#dmOJVS3P_i!^>eGaC@sw(Z',
        SQLALCHEMY_DATABASE_URI = DATABASE["SQLALCHEMY_DATABASE_URI"],
        SQLALCHEMY_TRACK_MODIFICATIONS = DATABASE["SQLALCHEMY_TRACK_MODIFICATIONS"],
        DEBUG = True,
        JWT_AUTH_USERNAME_KEY = "email",
        JWT_AUTH_URL_RULE = "/auth/login",
        JWT_SECRET_KEY = "j/6Ds!3#dmOJVS3P_i!^>eGaC@sw(Z"
    )
    
    app.url_map.strict_slashes = False

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Database
    if not database_exists(DATABASE["SQLALCHEMY_DATABASE_URI"]):
        create_database(DATABASE["SQLALCHEMY_DATABASE_URI"])

    from .models.user import User
    from .models.task import Task
    from .models.tokenblocklist import TokenBlockList
    from .database import db
    with app.app_context():
        db.init_app(app)
        db.create_all()

    # Blueprints
    from .blueprints import security, schedule, auth
    app.register_blueprint(security.bp)
    app.register_blueprint(schedule.bp)
    app.register_blueprint(auth.bp)

    # Swagger UI
    from .blueprints import swagger
    app.register_blueprint(swagger.swaggerui_blueprint)

    # JWT
    # jwt = JWT(app, User.authenticate, User.identity)
    jwt = JWTManager(app)
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = TokenBlockList.query.filter_by(jti=jti).first()
        return token is not None

    return app


