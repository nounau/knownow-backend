from json import dumps
from flask import Blueprint, Flask, request, jsonify
from datetime import datetime, timedelta, timezone
from bson import json_util
from app.authentication import bp
from app.authentication.service import AuthService
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager
from hmac import compare_digest
from app.users.service import UserService
from app.utils.jwt_helper import jwt

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
    return user.id


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return user_service.getUserById(id=identity)

@bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    user = authenticate(email, password)
    # def check_password(self, password):
    #     return compare_digest(password, "password")

    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_token(user)
    return jsonify({'access_token': access_token}), 200


@bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = user_service.getUserByUserName(username=username)
    if not user or not user.check_password(password):
        return jsonify("Wrong username or password"), 401

    # You can use the additional_claims argument to either add
    # custom claims or override default claims in the JWT.
    additional_claims = {"aud": "some_audience", "foo": "bar"}
    access_token = create_access_token(username, additional_claims=additional_claims)
    return jsonify(access_token=access_token)

@bp.route('/register', methods=['POST'])
def register():

    _json = request.json
    _uType = _json['uType']
    _userName = _json['userName']
    _password = _json['password']
    _email = _json['email']
    _name = _json['name']
    _birthdate = _json['birthdate']
    _currentLocation = _json['currentLocation']
    _city = _json['city']
    _degree = _json['degree']
    _startDate = _json['startDate']
    _endDate = _json['endDate']
    _companyName = _json['companyName']
    _workExperience = _json['workExperience']
    _interests = _json['interests']
    _languages = _json['languages']
    _photo = _json['photo']
    _savedQuestions = _json['savedQuestions']
    _questionsAsked = _json['questionsAsked']
    _answersGiven = _json['answersGiven']
    _rewards = _json['rewards']
    _guestIpAddress = _json['guestIpAddress']
    _lastActiveTimeStamp = datetime.utcnow()

    register_info_array = [_uType, _userName, _password, _email, _name, _birthdate, _currentLocation, _city, _degree, 
                           _startDate, _endDate, _companyName, _workExperience, _interests, _languages, _photo, 
                           _savedQuestions, _questionsAsked, _answersGiven, _rewards, _guestIpAddress, _lastActiveTimeStamp]

    if _userName and _email and _password and request.method == "POST":

        # _hashed_password = generate_password_hash(_password)

        id = auth_service.register(register_info_array)
        # id = mongo.db.user.insert_one({'uType':_uType, 'userName':_userName, 'password':_hashed_password, 'email':_email, 'name':_name,
        #                                'birthdate':_birthdate, 'currentLocation':_currentLocation, 'city':_city, 'degree':_degree, 'startDate':_startDate, 'endDate':_endDate,
        #                                'companyName':_companyName, 'workExperience':_workExperience, 'photo':_photo, 'guestIpAddress':_guestIpAddress, 'lastActiveTimeStamp':_lastActiveTimeStamp})

        return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
    else:
        return not_found()

@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Hello, {current_user}!'}), 200
