from flask import request
from flask_restx import Namespace, Resource, fields
from ..models import Student
from werkzeug.security import generate_password_hash, check_password_hash

from ..utils import db
from http import HTTPStatus
from ..utils.decorators import admin_required, get_user_type

student_namespace = Namespace('students', description='Student related operations')


student_model = student_namespace.model(
    'student', {
    'id': fields.Integer(required=True, description='Student ID'), 
    'name': fields.String(required=True, description='Student name'),
    'student_id': fields.String(required=True, description='Student ID'),
    'email': fields.String(required=True, description='Student email'),
    'user_type': fields.String(required=True, description='Student type')
    }
)

student_signup_model = student_namespace.model( 
    'student_signup', {
    'name': fields.String(required=True, description='Student name'),
    'student_id': fields.String(required=True, description='Student ID'),
    'email': fields.String(required=True, description='Student email'),
    'password': fields.String(required=True, description='Student password')
    }
)

@student_namespace.route('/')
class StudentList(Resource):
    @student_namespace.marshal_list_with(student_model)
    @admin_required
    def get(self):
        """Returns list of students"""
        student= Student.query.all()
        return student, HTTPStatus.OK
    

# @student_namespace.route ('/signup')
# class StudentSignup(Resource):
#     @student_namespace.expect(student_signup_model)
#     def post(self):
#         """Student signup"""
#         data = @student_namespace.payload
#         new_student = Student(name=data['name'], student_id=data['student_id'], email=data['email'], password_hash= generate_password_hash( data['password'],user_type='student')
#         new_student.save()
#         return {'message': 'Student created successfully'}, HTTPStatus.CREATED
    