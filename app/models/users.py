from app.factory.validation import Validator
from app.factory.database import Database


class Users(object):
    def __init__(self):
        self.validator = Validator()
        self.db = Database()

        self.collection_name = 'users'  # collection name

        self.fields = {
            "uType": "string",
            "userName": "string",
            "password": "string",
            "email": "string",
            "name": "string",
            "birthdate": "string",
            "currentLocation": "string",
            "city": "string",
            "degree": "string",
            "startDate": "datetime",
            "endDate": "datetime",
            "companyName": "string",
            "workExperience": "string",
            "interests": ["string"],
            "languages": ["string"],
            "photo": "string",
            "savedQuestions": ["string"],
            "questionsAsked": ["string"],
            "answersGiven": ["string"],
            "rewards": ["string"],
            "guestIpAddress": "string",
            "lastActiveTimeStamp": "datetime.datetime",
            "otpVerified": "bool"
        }

        self.create_required_fields = ["userName", "password", "email"]

        # Fields optional for CREATE
        self.create_optional_fields = []

        # Fields required for UPDATE
        self.update_required_fields = []

        # Fields optional for UPDATE
        self.update_optional_fields = []

    def create(self, user):
        # Validator will throw error if invalid
        self.validator.validate(user, self.fields, self.create_required_fields, self.create_optional_fields)
        res = self.db.insert(user, self.collection_name)
        return res

    def find(self, user):  
        return self.db.find(user, self.collection_name)

    def findByAggregate(self, user): 
        # Add logic to populate reference fields
        pipeline = [
            {"$match": user},
            {"$lookup": {"from": self.reference_fields["savedBy"]["collection"],
                         "localField": self.reference_fields["savedBy"]["localField"],
                         "foreignField": self.reference_fields["savedBy"]["foreignField"],
                         "as": self.reference_fields["savedBy"]["as"]}}
        ]

        return self.db.aggregate(pipeline, self.collection_name)

    def find_by_id(self, id):
        return self.db.find_by_id(id, self.collection_name)

    def update(self, id, user):
        self.validator.validate(user, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, user,self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)
