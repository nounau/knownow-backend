# services.py
from app.models import answers


class AnswerService:
    answers = answers.Answers()

    def get_all(self):
        return self.answers.find({})

    def getAnswerById(self, answer_id):
        return self.answers.find_by_id(answer_id)

    def postAnswer(self, data):
        # Add validation logic here if needed
        return self.answers.create(data)

    def updateAnswer(self, answer_id, data):
        # Add validation logic here if needed
        return self.answers.update(answer_id, data)

    def delete(self, answer_id):
        return self.answers.delete(answer_id)
