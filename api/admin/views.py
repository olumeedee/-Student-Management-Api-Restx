from flask_restx import Namespace, Resource, fields
from ..models.admin import Admin
from ..utils.decorators import admin_required
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity
from werkzeug.security import generate_password_hash


admin_namespace = Namespace('admin', description='Namespace for Administrators')

admin_signup_model = admin_namespace.model(
    'AdminSignup', {
        'name': fields.String(required=True),
        'email': fields.String(required=True),
        'password': fields.String(required=True)
    }
)

admin_model = admin_namespace.model(
    'Admin', {
        'id': fields.Integer,
        'name': fields.String(required=True),
        'email': fields.String(required=True),
        'user_type': fields.String(required=True)
    }
)


@admin_namespace.route('')
class GetAllAdmins(Resource):

        @admin_namespace.marshal_with(admin_model)
        @admin_required()
        def get(self):
            """
            Retrieve All Admins - Admins Only
            """
            admins = Admin.query.all()

            return admins, HTTPStatus.OK
    

@admin_namespace.route('/register')
class AdminRegistration(Resource):
          
        @admin_namespace.expect(admin_signup_model)
        @admin_required()
        def post(self):
            """
            Register an Admin - Admins Only, after First Admin
            """
            data = admin_namespace.payload

            admin = Admin.query.filter_by(email=data['email']).first()
            if admin:
                return {"message": "Admin Account Already Exists"}
    
            new_admin = Admin(
                name=data['name'],
                email=data['email'],
                password=generate_password_hash(data['password']),
                user_type='admin'
            )
    
            new_admin.save()
    
            return new_admin, HTTPStatus.CREATED
        

# @admin_namespace.route('/login')
# class AdminLogin(Resource):
        
#             @admin_namespace.expect(admin_signup_model)
#             def post(self):
#                 """
#                 Admin Login
#                     return {"message": "Invalid Credentials"}
        
#                 access_token = admin.encode_token(admin.id)
#                 return {"message": "Login Successful", "access_token": access_token}, HTTPStatus.OK
      
#                 """
#                 data = admin_namespace.payload
        
#                 admin = Admin.query.filter_by(email=data['email']).first()
#                 if not admin:
#                     return {"message": "Admin Account Does Not Exist"}
        
#                 if not admin.check_password(data['password']):
#                     return {"message": "Invalid Credentials"}
                
@admin_namespace.route('/<int:admin_id>')
class GetUpdateDeleteAdmins(Resource):
    
    @admin_namespace.marshal_with(admin_model)
    @admin_required()
    def get(self, admin_id):
        """
            Retrieve an Admin's Details by ID - Admins Only
        """
        admin = Admin.get_by_id(admin_id)
        
        return admin, HTTPStatus.OK
    
    @admin_namespace.expect(admin_signup_model)
    
    @admin_required()
    def put(self, admin_id):
        """
            Update an Admin's Details by ID - Admins Only
        """
        admin = Admin.get_by_id(admin_id)
        active_admin = get_jwt_identity()
        if active_admin != admin_id:
            return {"message": "Specific Admin Only"}, HTTPStatus.FORBIDDEN

        data = admin_namespace.payload

        admin.name = data['name']
        admin.email = data['email']
        admin.password_hash = generate_password_hash(data['password'])

        admin.update()

        admin_resp = {}
        admin_resp['id'] = admin.id
        admin_resp['name'] = admin.name
        admin_resp['email'] = admin.email
        admin_resp['user_type'] = admin.user_type

        return admin_resp, HTTPStatus.OK
    
   
    @admin_required()
    def delete(self, admin_id):
        """
            Delete an Admin by ID - Admins Only
        """
        admin = Admin.get_by_id(admin_id)

        admin.delete()

        return {"message": "Admin Successfully Deleted"}, HTTPStatus.OK