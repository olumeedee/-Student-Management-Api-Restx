from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed
from http import HTTPStatus
from .auth.views import auth_namespace
from .admin.views import admin_namespace
from .courses.views import course_namespace
from .students.views import student_namespace
from .config.config import config_dict
from .utils import db
from .models.users import User
from .models.admin import Admin
from .models.grades import Grade
from .models.courses import Course
from .models.students import Student
from .models.enrollment import Enrollment   


def create_app(config=config_dict['dev']):
    app = Flask(__name__)



    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {
            "message": "The token has expired",
            "error": "token_expired"
        }, HTTPStatus.UNAUTHORIZED
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {
            "message": "Token verification failed",
            "error": "invalid_token"
        }, HTTPStatus.UNAUTHORIZED
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {
            "message": "Request is missing an access token",
            "error": "authorization_required"
        }, HTTPStatus.UNAUTHORIZED
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback():
        return {
            "message": "The token is not fresh",
            "error": "fresh_token_required"
        }, HTTPStatus.UNAUTHORIZED

    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Add a JWT token to the header with ** Bearer &lt;JWT&gt; ** token to authorize"
        }
    }

    api = Api(
        app,
        title='A Student Management API',
        description='A student management API built with Flask, Flask-RESTX, Flask-JWT-Extended, and Flask-SQLAlchemy',
        authorizations=authorizations,
        security='Bearer Auth'
        )

    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(admin_namespace, path='/admin')
    api.add_namespace(course_namespace, path='/courses')
    api.add_namespace(student_namespace, path='/students')

    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method Not Allowed"}, HTTPStatus.NOT_FOUND

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Admin': Admin,
            'Grade': Grade,
            'Course': Course,
            'Student': Student,
            'Enrollment': Enrollment
        }
        

    return app