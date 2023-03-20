from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .students.views import student_namespace
from .config.config import config_dict
from .utils import db
from .models.users import User
from .models.student import Student
from .models.courses import Courses
from .models.enrollment import Enrollment
from .models.admin import Admin
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed

def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    jwt = JWTManager(app)


    migrate = Migrate(app, db)

    api = Api(app)
    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(student_namespace, path='/students')
    
    
    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"},404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method Not Allowed"},405




    app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Student': Student,
            'Courses': Courses,
            'Enrollment': Enrollment,
            'Admin': Admin,
        }

    

    return app