# services.py
from app.models import users


class UserService:
    users = users.Users()

    def get_all(self):
        return self.users.find({})

    def getUserById(self, user_id):
        return self.users.find_by_id(user_id)

    def postUser(self, data):
        # Add validation logic here if needed
        return self.users.create(data)

    def updateUser(self, user_id, data):
        # Add validation logic here if needed
        return self.users.update(user_id, data)

    def delete(self, user_id):
        return self.users.delete(user_id)
