# services.py
from app.models import questions


class QuestionService:
    questions = questions.Questions()

    def get_all(self):
        return self.questions.find({})

    def getQuestionById(self, question_id):
        return self.questions.find_by_id(question_id)

    def postQuestion(self, data):
        # Add validation logic here if needed
        return self.questions.create(data)

    def updateQuestion(self, question_id, data):
        # Add validation logic here if needed
        return self.questions.update(question_id, data)

    def delete(self, question_id):
        return self.questions.delete(question_id)
