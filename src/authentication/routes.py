from json import dumps
from flask import Blueprint, Flask, request, jsonify
from datetime import datetime, timedelta, timezone
from bson import json_util
from src.authentication import bp
from src.authentication.service import AuthService
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager
from hmac import compare_digest
from src.models.otp import Otp
from src.users.service import UserService
from src.utils.jwt_helper import jwt
from flask_jwt_extended import current_user

auth_service = AuthService()
user_service = UserService()

def authenticate(email, password):
    return auth_service.authenticate(email, password);
    
def create_token(user):
    token = create_access_token(identity=user['email'])
    return token

# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user._id


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return user_service.getUserById(user_id=identity)

# @bp.route('/login', methods=['POST'])
# def login():
#     email = request.json.get('email', None)
#     password = request.json.get('password', None)

#     user = authenticate(email, password)
#     # def check_password(self, password):
#     #     return compare_digest(password, "password")

#     if not user:
#         return jsonify({'error': 'Invalid credentials'}), 401

#     access_token = create_token(user)
#     return jsonify({'access_token': access_token}), 200


@bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("userName", None)
    password = request.json.get("password", None)
    user = user_service.getUserByUserName(user_name=username)
    if not user or not user.check_password(password):
        return jsonify("Wrong username or password"), 401

    # You can use the additional_claims argument to either add
    # custom claims or override default claims in the JWT.
    additional_claims = {"foo": "bar"}
    access_token = create_access_token(user, additional_claims=additional_claims)
    return jsonify(access_token=access_token)


@bp.route("/who_am_i", methods=["GET"])
@jwt_required()
def protected():
    # We can now access our sqlalchemy User object via `current_user`.
    return jsonify(
        id=current_user._id,
        full_name=current_user.name,
        userName=current_user.userName,
        email=current_user.email,
        currentLocation= current_user.currentLocation
    )

@bp.route('/verifyOTP', methods=['GET'])
def verifyOTP():
    email_of_OTP = request.json.get('email', None)
    if(Otp().get_otp(email_of_OTP) == request.json.get('otp', None)):
        # otp.updateStatus(email_of_OTP, "INACTIVE")
        auth_service.updateOtpVerifiedFlag(email_of_OTP, True)
        return jsonify({'success': True, 'message': 'OTP verified!', 'response': ''}), 200
    else:
        return jsonify({'success': False, 'message': 'OTP verification failed!!', 'response': ''}), 401