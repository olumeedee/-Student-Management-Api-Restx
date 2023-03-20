from flask_restx import Namespace,Resource, fields
from flask import request
from ..models.users import User
from ..utils import db
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity


auth_namespace = Namespace('auth', description='Authentication related operations')


user_model = auth_namespace.model(
    'User', {
        'id': fields.Integer(description='The user unique identifier'),
        'username': fields.String(required=True, description='The user username'),
        'email': fields.String(required=True, description='The user email'),
        'password_hash': fields.String(required=True, description='The user password'),
        "user_type": fields.String(required=True, description="Type of User")

    }
)

login_model = auth_namespace.model(
    'Login', {
        'email': fields.String(required=True, description='The user email'),
        'password': fields.String(required=True, description='The user password'),
    }
)




@auth_namespace.route('/login')
class Login(Resource):

    @auth_namespace.expect(login_model)
    def post(self):
        """
            Login a user
        """

        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        user=User.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password_hash, password):
            
                access_token =create_access_token(identity=user.username)
                refresh_token=create_refresh_token(identity=user.username)

                response = {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }

                return response, HTTPStatus.OK

@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        username = get_jwt_identity()
        access_token = create_access_token(identity=username)
        return {'access_token': access_token}, HTTPStatus.OK