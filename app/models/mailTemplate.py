from app.factory.validation import Validator
from app.factory.database import Database


class MailTemplate(object):
    def __init__(self):
        self.validator = Validator()
        self.db = Database()

        self.collection_name = 'mailTemplate'  # collection name

        self.fields = {
            "mailType": "string",
            "subject": "string",
            "description": "string",
            "created": "datetime",
            "updated": "datetime",
        }

        self.create_required_fields = ["mailType", "subject", "description"]

        # Fields optional for CREATE
        self.create_optional_fields = []

        # Fields required for UPDATE
        self.update_required_fields = []

        # Fields optional for UPDATE
        self.update_optional_fields = []

    def create(self, mailTemplate):
        # Validator will throw error if invalid
        self.validator.validate(mailTemplate, self.fields, self.create_required_fields, self.create_optional_fields)
        res = self.db.insert(mailTemplate, self.collection_name)
        return res

    def find(self, mailTemplate):  
        return self.db.find(mailTemplate, self.collection_name)

    # def findByAggregate(self, question): 
    #     # Add logic to populate reference fields
    #     pipeline = [
    #         {"$match": question},
    #         {"$lookup": {"from": self.reference_fields["savedBy"]["collection"],
    #                      "localField": self.reference_fields["savedBy"]["localField"],
    #                      "foreignField": self.reference_fields["savedBy"]["foreignField"],
    #                      "as": self.reference_fields["savedBy"]["as"]}}
    #     ]

    #     return self.db.aggregate(pipeline, self.collection_name)

    def find_by_mailType(self, type):
        return self.db.find_one_by_fieldname("mailType", type, self.collection_name)

    def update(self, id, mailTemplate):
        self.validator.validate(mailTemplate, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, mailTemplate,self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)
