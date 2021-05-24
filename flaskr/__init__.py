import os
from flask import Flask, url_for, jsonify
from sqlalchemy_utils import create_database, database_exists
from flask_jwt_extended import JWTManager
from .models.tokenblocklist import TokenBlockList

def create_app(test_config=False):
    app = Flask(__name__, instance_relative_config=True)
    
    app.url_map.strict_slashes = False

    if not test_config:
        # load the instance config, if it exists, when not testing
        app.config.from_object(os.environ.get("APP_SETTINGS"))

        # Database
        if not database_exists(os.environ.get("SQLALCHEMY_DATABASE_URI")):
            create_database(os.environ.get("SQLALCHEMY_DATABASE_URI"))

        from .models.user import User
        from .models.task import Task
        from .database import db
        with app.app_context():
            db.init_app(app)
            db.create_all()
    else:
        # load the test config if passed in
        app.config.from_object(os.environ.get("APP_SETTINGS_TEST"))

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Blueprints
    from .blueprints import security, schedule, auth
    app.register_blueprint(security.bp)
    schedule.configure(app)
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
        token = TokenBlockList.get_by_token(jti)
        return token is not None

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({"message": "say hello"})

    return app


