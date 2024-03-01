from datetime import datetime 
from app.factory.validation import Validator
from app.factory.database import Database
from hmac import compare_digest

class Users(object):
    def __init__(self, _id=None, uType=None, userName=None, password=None, email=None, name=None,
                 birthdate=None, currentLocation=None, city=None, degree=None, startDate=None, endDate=None,
                 companyName=None, workExperience=None, interests=None, languages=None, photo=None,
                 savedQuestions=None, questionsAsked=None, answersGiven=None, rewards=None, guestIpAddress=None,
                 lastActiveTimeStamp=None, otpVerified=None):
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

        self._id = _id
        self.uType = uType
        self.userName = userName
        self.password = password
        self.email = email
        self.name = name
        self.birthdate = birthdate
        self.currentLocation = currentLocation
        self.city = city
        self.degree = degree
        self.startDate = startDate
        self.endDate = endDate
        self.companyName = companyName
        self.workExperience = workExperience
        self.interests = interests
        self.languages = languages
        self.photo = photo
        self.savedQuestions = savedQuestions
        self.questionsAsked = questionsAsked
        self.answersGiven = answersGiven
        self.rewards = rewards
        self.guestIpAddress = guestIpAddress
        self.lastActiveTimeStamp = lastActiveTimeStamp
        self.otpVerified = otpVerified

    def __repr__(self):
        return f"Users(user_id={self._id}, userName={self.userName}, email={self.email}, " \
               f"lastActiveTimeStamp={self.lastActiveTimeStamp}, otpVerified={self.otpVerified})"

    def map_document_to_instance(self, document):
        """
        Map a MongoDB document to an instance of the Users class.
        """
        if not document:
            return None

        user_instance = Users()
        for field, value in document.items():
            if isinstance(value, list):
                setattr(user_instance, field, [str(item) for item in value])
            elif isinstance(value, dict):
                # Assuming nested dictionaries are not handled in this example
                # You may need to recursively map nested dictionaries
                pass
            else:
                setattr(user_instance, field, value)

        return user_instance

    def create(self, user):
        # Validator will throw error if invalid
        user["otpVerified"] = False
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
        return self.map_document_to_instance(self.db.find_by_id(id, self.collection_name))

    # NOTE: In a real application make sure to properly hash and salt passwords
    def check_password(self, password):
        # return compare_digest( self.password, password)
        return self.password == password
    def find_by_username(self, username):
        return self.map_document_to_instance(self.db.find_one_by_fieldname("userName", username, self.collection_name))
    
    def find_by_email(self, email):
        return self.map_document_to_instance(self.db.find_one_by_fieldname("email", email, self.collection_name))

    def updateOtpVerifiedFlag(self, email_of_OTP, otpVerified):
        criteria = {"email": email_of_OTP}
        element = {
            "otpVerified": otpVerified,
            "updated": datetime.now()  # Update the 'updated' field
        }
        return self.db.update_by_criteria(criteria, element, self.collection_name)

    def update(self, id, user):
        self.validator.validate(user, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, user, self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)
