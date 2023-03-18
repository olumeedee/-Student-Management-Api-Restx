from flask import Flask
from .config.config import config_dict
from flask_restx import Api
from .auth.views import auth_namespace
from .courses.views import  courses_namespace



def create_app(config=config_dict['dev']):
    app = Flask(__name__) 
    
    app.config.from_object(config)

    api=Api(app)

    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(courses_namespace, path='/courses')

    return app
    app.run(debug=True)

