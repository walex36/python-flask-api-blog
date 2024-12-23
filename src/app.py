import os
from flask import Flask, json
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from src.models import db
from flask_bcrypt import Bcrypt
from werkzeug.exceptions import HTTPException
from flask_marshmallow import Marshmallow
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin


migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
ma = Marshmallow()
spec = APISpec(
    title="Blog API",
    version="1.0.0",
    openapi_version="3.0.2",
    info=dict(description="Blog API Documentation"),
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)


def create_app(environment=os.environ["ENVIRONMENT"]):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f'src.config.{environment.title()}Config')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)

    # register blueprints
    from src.controllers import user, post, auth
    app.register_blueprint(user.app)
    app.register_blueprint(post.app)
    app.register_blueprint(auth.app)
    
    @app.route("/docs")
    def docs():
        return spec.path(view=user.handler_user_id).path(view=user.handler_user).to_dict()
    
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response
        
    return app
    # a simple page that says hello