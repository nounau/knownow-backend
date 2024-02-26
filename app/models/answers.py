from app.factory.validation import Validator
from app.factory.database import Database


class Answers(object):
    def __init__(self):
        self.validator = Validator()
        self.db = Database()

        self.collection_name = 'questions'  # collection name

        self.fields = {
            "title": "string",
            # "savedBy": "string",
            "description": "string",
            "noOfReposts": "string",
            "tags": ["string"],
            "isRealTime": "bool",
            # "views": "string",
            "created": "datetime",
            "updated": "datetime",
        }

        self.create_required_fields = ["title"]

        # Fields optional for CREATE
        self.create_optional_fields = []

        # Fields required for UPDATE
        self.update_required_fields = ["title"]

        # Fields optional for UPDATE
        self.update_optional_fields = []

    def create(self, question):
        # Validator will throw error if invalid
        self.validator.validate(question, self.fields, self.create_required_fields, self.create_optional_fields)
        res = self.db.insert(question, self.collection_name)
        return res

    def find(self, question):  
        return self.db.find(question, self.collection_name)

    def findByAggregate(self, question): 
        # Add logic to populate reference fields
        pipeline = [
            {"$match": question},
            {"$lookup": {"from": self.reference_fields["savedBy"]["collection"],
                         "localField": self.reference_fields["savedBy"]["localField"],
                         "foreignField": self.reference_fields["savedBy"]["foreignField"],
                         "as": self.reference_fields["savedBy"]["as"]}}
        ]

        return self.db.aggregate(pipeline, self.collection_name)

    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)

    def update(self, id, question):
        self.validator.validate(question, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, question,self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)
