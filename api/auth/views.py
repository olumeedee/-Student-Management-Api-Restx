from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.users import User
from ..utils.decorators import admin_required
from werkzeug.security import check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

auth_namespace = Namespace('auth', description='Namespace for Authentication')

user_model = auth_namespace.model(
    'User', {
        'id': fields.Integer(description="User ID"),
        'name': fields.String(required=True),
        'email': fields.String(required=True),
        'password_hash': fields.String(required=True),
        'user_type': fields.String(required=True, )  
    }
)

login_model = auth_namespace.model(
    'Login', {
        'email': fields.String(required=True),
        'password': fields.String(required=True)
    }
)

@auth_namespace.route('/users')
class GetAllUsers(Resource):
    @auth_namespace.marshal_with(user_model)

    @admin_required()
    def get(self):
        """
            Retrieve all Users - Admins  allowed only

        """
        users = User.query.all()

        return users, HTTPStatus.OK

@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
            Generate JWT  Access Token 
        """
        data = auth_namespace.payload

        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            return response, HTTPStatus.CREATED


@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
            Genete JWT Refresh Token
        """
        user = get_jwt_identity()

        access_token = create_access_token(identity=user)

        return {'access_token': access_token}, HTTPStatus.OK


