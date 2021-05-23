import os
from flask import Flask, url_for, jsonify
from sqlalchemy_utils import create_database, database_exists
from flask_jwt import JWT
from .models.user import User
from .config import *

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='j/6Ds!3#dmOJVS3P_i!^>eGaC@sw(Z',
        SQLALCHEMY_DATABASE_URI = DATABASE["SQLALCHEMY_DATABASE_URI"],
        SQLALCHEMY_TRACK_MODIFICATIONS = DATABASE["SQLALCHEMY_TRACK_MODIFICATIONS"],
        DEBUG = True,
        JWT_AUTH_USERNAME_KEY = "email",
        JWT_AUTH_URL_RULE = "/auth/login"
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
    from .database import db
    with app.app_context():
        db.init_app(app)
        db.create_all()

    # Blueprints
    from .blueprints import security
    app.register_blueprint(security.bp)
    from .blueprints import schedule
    app.register_blueprint(schedule.bp)

    # Swagger UI
    from .blueprints import swagger
    app.register_blueprint(swagger.swaggerui_blueprint)

    # JWT
    jwt = JWT(app, User.authenticate, User.identity)


    @app.route("/site-map")
    def site_map():
        links = []
        for rule in app.url_map.iter_rules():
            # Filter out rules we can't navigate to in a browser
            # and rules that require parameters
            if "GET" in rule.methods and has_no_empty_params(rule):
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                links.append((url, rule.endpoint))
        return jsonify(links)

    return app

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)