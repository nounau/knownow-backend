from app.factory.validation import Validator
from app.factory.database import Database
from bson import ObjectId

class SavedBy(object):
    def __init__(self):
        self.validator = Validator()
        self.db = Database()

        self.collection_name = 'savedBy'  # collection name

        self.fields = {
            "userId": "string",
            "questionId": "string",
            "created": "datetime",
            "updated": "datetime",
        }

        self.create_required_fields = ["userId", "questionId"]

        # Fields optional for CREATE
        self.create_optional_fields = []

        # Fields required for UPDATE
        self.update_required_fields = [""]

        # Fields optional for UPDATE
        self.update_optional_fields = []

    def savedBy(self, current_user, questionId):
        result = self.db.find_one({'userId':current_user}, self.collection_name)
        if result:
            if questionId not in result['questionIds']:
                result['questionIds'].append(questionId)
                print(result['questionIds'])
                self.db.update_by_criteria({'userId':current_user}, {'questionIds':result['questionIds']}, self.collection_name)
                return "Question added to User!"
            else:
                return "Question already saved"
        else:
            self.db.insert({'userId':current_user, 'questionIds':[questionId]}, self.collection_name)
        return result

    def create(self, savedBy):
        # Validator will throw error if invalid
        self.validator.validate(savedBy, self.fields, self.create_required_fields, self.create_optional_fields)
        res = self.db.insert(savedBy, self.collection_name)
        return res

    def find(self, savedBy):  
        return self.db.find(savedBy, self.collection_name)

    def findByAggregate(self, savedBy): 
        # Add logic to populate reference fields
        pipeline = [
            {"$match": savedBy},
            {"$lookup": {"from": self.reference_fields["savedBy"]["collection"],
                         "localField": self.reference_fields["savedBy"]["localField"],
                         "foreignField": self.reference_fields["savedBy"]["foreignField"],
                         "as": self.reference_fields["savedBy"]["as"]}}
        ]

        return self.db.aggregate(pipeline, self.collection_name)

    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)

    def update(self, id, savedBy):
        self.validator.validate(savedBy, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, savedBy,self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)
