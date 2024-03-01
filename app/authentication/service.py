# services.py
from app.models import questions
from app.models import users


class AuthService:
    questions = questions.Questions()
    users = users.Users()

    def authenticate(self,email, password):
        user = {'email': "rohansharma996034@gmail.com", "password": "password"} # add logic to fetch password from database Here
        if user and user['password'] == password:
            return {'email': user['email']}
        else:
            return None
        return self.questions.find({})

    # def getQuestionById(self, question_id):
    #     return self.questions.find_by_id(question_id)

    # def postQuestion(self, data):
    #     # Add validation logic here if needed
    #     return self.questions.create(data)

    # def updateQuestion(self, question_id, data):
    #     # Add validation logic here if needed
    #     return self.questions.update(question_id, data)

    # def delete(self, question_id):
    #     return self.questions.delete(question_id)
    
    def updateOtpVerifiedFlag(self, email_of_OTP, otpVerified):
        return self.users.updateOtpVerifiedFlag(email_of_OTP, otpVerified)
