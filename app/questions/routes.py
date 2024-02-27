from json import dumps
from app.questions.service import QuestionService
from flask import Blueprint, Flask, request, jsonify
from datetime import datetime, timedelta, timezone
from bson import json_util
from app.questions import bp

question_service = QuestionService()

@bp.route('/questions/postquestion', methods=['POST'])
def postQuestion():
    questionData = request.get_json()
    _title = questionData['title']

    if _title and request.method == "POST":

        id = question_service.postQuestion(questionData)
        
        return jsonify({'ok': True, 'message': 'Question created successfully!', 'response': id}), 200
    return jsonify({'ok': False, 'message': 'Something went wrong', 'response': ''}), 400
    
@bp.route('/questions/<string:id>', methods=['GET'])
def getQuestion(id):
    question = question_service.getQuestionById(id)
    if question:
        resp = question
        #json.loads(json_util.dumps(data))
        return jsonify({'ok': True, 'message': 'Question Fetched!', 'response': resp}), 200
    return jsonify({'ok': False, 'message': 'Something went wrong', 'response': ''}), 400
    
@bp.route('/questions/', methods=['GET'])
def getAllQuestions():
    question = question_service.get_all()
    if question:
        resp = question
        #json.loads(json_util.dumps(data))
        return jsonify({'ok': True, 'message': 'All Questions Fetched!', 'response': resp}), 200
    return jsonify({'ok': False, 'message': 'Something went wrong', 'response': ''}), 400
    
@bp.route('/questions/<id>', methods=['PUT'])
def editQuestion(id):
    
    questionData = request.get_json()
    _title = questionData['title']

    if _title:
        
        id = question_service.updateQuestion(id,questionData)        
        return jsonify({'ok': True, 'message': 'Question updated successfully!', 'response': id}), 200
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
    
