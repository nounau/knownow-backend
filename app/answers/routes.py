from json import dumps
from flask import Blueprint, Flask, request, jsonify
from datetime import datetime, timedelta, timezone
from app.answers import service
from bson import json_util
from app.answers import bp

@bp.route('/postanswer', methods=['POST'])
def postAnswer():
    _json = request.json
    _questionId = _json['questionId']
    _answer = _json['answer']
    _userId = _json['userId']
    _likes = _json['likes']
    _comments = _json['comments']
    _createdTimeStamp = _json['createdTimeStamp']
    _updatedTimeStamp = _json['updatedTimeStamp']
    _isQualifiedRealTime = _json['isQualifiedRealTime']

    if _questionId and _answer:

        id = service.postAnswer(answer_info_array)
        # id = mongo.db.questions.insert_one({'title':_title, 'uId':_uId, 'noOfReposts':_noOfReposts, 'isRealTime':_isRealTime, 
        #                            'createdTimeStamp':_createdTimeStamp, 'updatedTimeStamp':_updatedTimeStamp, 'tags':_tags})
        
        return jsonify({'ok': True, 'message': 'Answer posted successfully!'}), 200
    else:
        return not_found()

@bp.route('/getanswer/<id>', methods=['GET'])
def getAnswer(id):
    ans = service.getAnswerById(id)
    if ans:
        resp = json_util.dumps(ans)
        #json.loads(json_util.dumps(data))
        return resp
    else:
        return not_found()

@bp.route('/updateanswer/<id>', methods=['PUT'])
def editAnswer(id):
    _id = id
    _json = request.json
    _questionId = _json['questionId']
    _answer = _json['answer']
    _userId = _json['userId']
    _likes = _json['likes']
    _comments = _json['comments']
    _createdTimeStamp = datetime.utcnow()
    _updatedTimeStamp = datetime.utcnow()
    _isQualifiedRealTime = _json['isQualifiedRealTime']

    answer_info_array = [_id, _questionId, _answer, _userId, _likes, _comments, _createdTimeStamp, _updatedTimeStamp, _isQualifiedRealTime]

    if _questionId and _answer and request.method == "POST":

        id = service.updateAnswer(answer_info_array)
        # id = mongo.db.questions.insert_one({'title':_title, 'uId':_uId, 'noOfReposts':_noOfReposts, 'isRealTime':_isRealTime, 
        #                            'createdTimeStamp':_createdTimeStamp, 'updatedTimeStamp':_updatedTimeStamp, 'tags':_tags})
        
        return jsonify({'ok': True, 'message': 'Answer updated successfully!'}), 200
    else:
        return not_found()

@bp.errorhandler(404)
def not_found(error=None):
    message = {
        'status':404,
        'message':'Not Found' + request.url
    }
    resp = jsonify(message)
 
    resp.status_code = 404
 
    return resp