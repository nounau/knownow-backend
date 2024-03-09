from datetime import datetime, timedelta
import traceback
from src.factory.validation import Validator
from src.factory.database import Database


class Otp(object):
    def __init__(self):
        self.validator = Validator()
        self.db = Database()

        self.collection_name = 'otp'  # collection name

        self.fields = {
            "email":"string",
            "otp": "string", 
            "expTime": "datetime", 
            "status": "string",
            "created": "datetime",
            "updated": "datetime",
        }

        self.create_required_fields = ["email", "otp"]

        # Fields optional for CREATE
        self.create_optional_fields = []

        # Fields required for UPDATE
        self.update_required_fields = ["otp"]

        # Fields optional for UPDATE
        self.update_optional_fields = []

    def save_otp(self, email, OTP):
        # Validator will throw error if invalid
        # self.validator.validate(otp, self.fields, self.create_required_fields, self.create_optional_fields)
        criteria = {"email": email}
        element = {
            "OTP": OTP,
            "exp_Time": datetime.now() + timedelta(minutes=5),
            "updated": datetime.now()  # Update the 'updated' field
        }
        res = self.db.upsert_by_criteria(criteria, element, self.collection_name)
        return res

    def get_otp(self, email):
        try:
            otpObj = self.db.find_one({"email":email, "exp_Time":{'$gte': datetime.now()}}, self.collection_name)
            print(otpObj)
            if otpObj:
                return otpObj.get('OTP')
            else:
                return None
        except TypeError:
            print("No OTP Found!")
            return False
        
    def updateFlag(self, email, status):
        try:
            return self.db.update_status_by_email(email, status, self.collection_name)
        except Exception as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
