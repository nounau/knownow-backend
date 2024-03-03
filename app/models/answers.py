from app.factory.validation import Validator
from app.factory.database import Database


class Answers(object):
    def __init__(self):
        self.validator = Validator()
        self.db = Database()

        self.collection_name = 'answers'  # collection name

        self.fields = {
            "questionId" : "string",
            "answer" : "string",
            "userId" : "string",
            "likes" : "int",
            "comments" : ["string"],
            "isQualifiedRealTime" : "bool"
        }

        self.create_required_fields = ["questionId","answer","userId"]

        # Fields optional for CREATE
        self.create_optional_fields = []

        # Fields required for UPDATE
        self.update_required_fields = ["answer"]

        # Fields optional for UPDATE
        self.update_optional_fields = []

    def create(self, answer):
        # Validator will throw error if invalid
        # self.validator.validate(answer, self.fields, self.create_required_fields, self.create_optional_fields)
        res = self.db.insert(answer, self.collection_name)
        return res

    def find(self, answer):  
        return self.db.find(answer, self.collection_name)
    
    def getAllAnswersForCurrentUser(self, current_user):
        return self.db.find_many_by_fieldname("userId", current_user, self.collection_name)

    def findByAggregate(self, answer): 
        # Add logic to populate reference fields
        pipeline = [
            {"$match": answer},
            {"$lookup": {"from": self.reference_fields["savedBy"]["collection"],
                         "localField": self.reference_fields["savedBy"]["localField"],
                         "foreignField": self.reference_fields["savedBy"]["foreignField"],
                         "as": self.reference_fields["savedBy"]["as"]}}
        ]

        return self.db.aggregate(pipeline, self.collection_name)

    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)

    def update(self, id, answer):
        self.validator.validate(answer, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, answer,self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)
