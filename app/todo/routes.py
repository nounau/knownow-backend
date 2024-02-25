# controller.py
from flask import request, jsonify
from app.todo import bp
from app.todo.service import TodoService
from bson.json_util import dumps

todo_service = TodoService()

@bp.route('/todos/', methods=['GET'])
def get_tasks():
    return jsonify(todo_service.get_all()), 200

@bp.route('/todos/<string:todo_id>/', methods=['GET'])
def get_task(todo_id):
    return todo_service.get_by_id(todo_id), 200

@bp.route('/todos/', methods=['POST'])
def add_tasks():
    data = request.get_json()
    # title = request.form['title']
    # body = request.form['body']
    response = todo_service.create(data)
    return jsonify(response), 201

@bp.route('/todos/<string:todo_id>/', methods=['PUT'])
def update_tasks(todo_id):
    if request.method == "PUT":
        title = request.form['title']
        body = request.form['body']
        response = todo_service.update(todo_id, {'title': title, 'body': body})
        return response, 201

@bp.route('/todos/<string:todo_id>/', methods=['DELETE'])
def delete_tasks(todo_id):
    if request.method == "DELETE":
        todo_service.delete(todo_id)
        return "Record Deleted"
