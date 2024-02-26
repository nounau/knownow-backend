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
    # _uId = questionData['uId']
    # _savedBy = questionData['savedBy']
    # _noOfReposts = questionData['noOfReposts']
    # _isRealTime = questionData['isRealTime']
    # _createdTimeStamp = datetime.utcnow()
    # _updatedTimeStamp = datetime.utcnow()
    # _tags = questionData['tags']
    # _views = questionData['views']

    if _title and request.method == "POST":

        id = question_service.postQuestion(questionData)
        # id = mongo.db.questions.insert_one({'title':_title, 'uId':_uId, 'noOfReposts':_noOfReposts, 'isRealTime':_isRealTime, 
        #                            'createdTimeStamp':_createdTimeStamp, 'updatedTimeStamp':_updatedTimeStamp, 'tags':_tags})
        return jsonify({'ok': True, 'message': 'Question created successfully!'}), 200
    
@bp.route('/questions/<string:id>', methods=['GET'])
def getQuestion(id):
    question = question_service.getQuestionById(id)
    if question:
        resp = question
        #json.loads(json_util.dumps(data))
        return resp
    
@bp.route('/questions/', methods=['GET'])
def getAllQuestions():
    question = question_service.get_all()
    if question:
        resp = question
        #json.loads(json_util.dumps(data))
        return resp
    
@bp.route('/questions/<id>', methods=['PUT'])
def editQuestion(id):
    # _id = id
    # _json = request.json
    # _title = _json['title']
    # _uId = _json['uId']
    # _savedBy = _json['savedBy']
    # _noOfReposts = _json['noOfReposts']
    # _isRealTime = _json['isRealTime']
    # _createdTimeStamp = datetime.utcnow()
    # _updatedTimeStamp = datetime.utcnow()
    # _tags = _json['tags']
    # _views = _json['views']

    # question_info_array = [_id, _title, _uId, _savedBy, _noOfReposts, _isRealTime, _createdTimeStamp, _updatedTimeStamp, _tags, _views]

    questionData = request.get_json()
    _title = questionData['title']

    if _title:
        
        id = question_service.updateQuestion(id,questionData)        
        return jsonify({'ok': True, 'message': 'Question updated successfully!'}), 200
    return "failed"


@bp.errorhandler(404)
def not_found(error=None):
    message = {
        'status':404,
        'message':'Not Found custom' + request.url
    }
    resp = jsonify(message)
 
    resp.status_code = 404
 
    return resp