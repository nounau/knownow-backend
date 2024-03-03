from json import dumps
import json
from flask import Blueprint, Flask, request, jsonify
from datetime import datetime, timedelta, timezone

from flask_jwt_extended import get_jwt_identity, jwt_required
from app.answers import service
from bson import json_util
from app.answers import bp

service = service.AnswerService()

@bp.route('/answers/postanswer', methods=['POST'])
@jwt_required()
def postAnswer():
    _json = request.json
    _json['userId'] = get_jwt_identity()

    id = service.postAnswer(_json)
    if id:
        return jsonify({'ok': True, 'message': 'Answer posted successfully!', 'response': id}), 200
    return jsonify({'ok': False, 'message': 'Something went wrong', 'response': ''}), 400

@bp.route('/answers/<id>', methods=['GET'])
@jwt_required()
def getAnswer(id):
    ans = service.getAnswerById(id)
    if ans:
        return jsonify({'ok': True, 'message': 'Answer fetched successfully!', 'response': ans}), 200
    return jsonify({'ok': False, 'message': 'Something went wrong', 'response': ''}), 400

@bp.route('/answers/', methods=['GET'])
@jwt_required()
def getAllAnswersForCurrentUser():
    current_user = get_jwt_identity()
    print(current_user)
    if not current_user:
        return jsonify({'success': False, 'message': 'UnAutorized Access', 'response': ''}), 401
    
    if request.method == "GET":
        ans = service.getAllAnswersForCurrentUser(current_user)
        if ans:
            # resp = json_util.dumps(ans)
            resp = json.loads(json_util.dumps(ans))
            return jsonify({'success': True, 'message': 'Fetched all answers ', 'response': resp}), 200
        return jsonify({'ok': True, 'message': 'No Answers Found', 'response': ''}), 200
    else:
        return not_found()

@bp.route('/answers/<id>', methods=['PUT'])
@jwt_required()
def editAnswer(id):
    
    answerData = request.get_json()
    # questionId = answerData['questionId']

    if id:
        _id = service.updateAnswer(id, answerData)        
        return jsonify({'ok': True, 'message': 'Answer updated successfully!', 'response': _id}), 200
    return jsonify({'ok': False, 'message': 'Something went wrong', 'response': ''}), 400

@bp.errorhandler(404)
def not_found(error=None):
    message = {
        'status':404,
        'message':'Not Found' + request.url
    }
    resp = jsonify(message)
 
    resp.status_code = 404
 
    return resp