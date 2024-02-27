from json import dumps
from app.users.service import UserService
from flask import Blueprint, Flask, request, jsonify
from datetime import datetime, timedelta, timezone
from bson import json_util
from app.users import bp

user_service = UserService()

@bp.route('/users/postuser', methods=['POST'])
def postUser():
    userData = request.get_json()

    if request.method == "POST":

        id = user_service.postUser(userData)
        
        return jsonify({'ok': True, 'message': 'User created successfully!', 'response': id}), 200
    return jsonify({'ok': False, 'message': 'Something went wrong', 'response': ''}), 400
    
@bp.route('/users/<string:id>', methods=['GET'])
def getUser(id):
    user = user_service.getUserById(id)
    if user:
        resp = user
        #json.loads(json_util.dumps(data))
        return jsonify({'ok': True, 'message': 'User Fetched!', 'response': resp}), 200
    return jsonify({'ok': False, 'message': 'Something went wrong', 'response': ''}), 400
    
@bp.route('/users/', methods=['GET'])
def getAllUsers():
    user = user_service.get_all()
    if user:
        resp = user
        #json.loads(json_util.dumps(data))
        return jsonify({'ok': True, 'message': 'All Users Fetched!', 'response': resp}), 200
    return jsonify({'ok': False, 'message': 'Something went wrong', 'response': ''}), 400
    
@bp.route('/users/updateUser/<id>', methods=['PUT'])
def editUser(id):
    
    userData = request.get_json()

    if 'email' and 'password' not in userData:
        
        id = user_service.updateUser(id,userData)        
        return jsonify({'ok': True, 'message': 'User updated successfully!', 'response': id}), 200
    return jsonify({'ok': False, 'message': 'Something went wrong', 'response': ''}), 400

@bp.route('/users/deleteUser/<id>', methods=['DELETE'])
def deleteUser(id):
    
    dId = user_service.delete(id)  
    if(dId):
        return jsonify({'ok': True, 'message': 'User deleted successfully!', 'response': id}), 200
    return jsonify({'ok': False, 'message': 'Something went wrong', 'response': ''}), 400

# @bp.route('/questions/savedby', methods=['POST'])
# def savedBy():
#     # current_user = get_jwt_identity()
#     # if not current_user:
#     #     return jsonify({'success': False, 'message': 'UnAutorized Access', 'response': ''}), 401
#     _json = request.json
#     questionId = _json['questionId']

#     if current_user and questionId and request.method == "POST":
#         questionSavedBy = q_service.savedBy(current_user, questionId)
#         userQuestionsSaved = Service.questionsSaved(current_user, questionId)
#         # result = questionSavedBy + userQuestionsSaved
#         return jsonify({'ok': True, 'message': 'Saved By fetched', 'response': userQuestionsSaved}), 200
#     else:
#         return jsonify({'ok': False, 'message': 'Something went wrong', 'response': ''}), 400
    

@bp.errorhandler(404)
def not_found(error=None):
    message = {
        'status':404,
        'message':'Not Found custom' + request.url
    }
    resp = jsonify(message)
 
    resp.status_code = 404
 
    return resp