# services.py
from app.models import todo


class TodoService:
    todo = todo.Todo()

    def get_all(self):
        return self.todo.find({})

    def get_by_id(self, todo_id):
        return self.todo.find_by_id(todo_id)

    def create(self, data):
        # Add validation logic here if needed
        return self.todo.create(data)

    def update(self, todo_id, data):
        # Add validation logic here if needed
        return self.todo.update(todo_id, data)

    def delete(self, todo_id):
        return self.todo.delete(todo_id)
