from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from dynaconf import settings

from src.modules.common.mongo_utils import mongo_utils

client = MongoClient(settings.MONGO_DB_URL)
db = client['Users'] # Change this!
users = db['user']

class auth_data:

    @staticmethod
    def authenticate(email, password):
        user = users.find_one({'email': email})
        if user and user['password'] == password:
            return {'email': user['email']}
        else:
            return None
    
    @staticmethod
    def register(ria):

        _uType = ria[0]
        _userName = ria[1]
        _password = generate_password_hash(ria[2])
        _email = ria[3]
        _name = ria[4]
        _birthdate = ria[5]
        _currentLocation = ria[6]
        _city = ria[7]
        _degree = ria[8]
        _startDate = ria[9]
        _endDate = ria[10]
        _companyName = ria[11]
        _workExperience = ria[12]
        _interests = ria[13]
        _languages = ria[14]
        _photo = ria[15]
        _savedQuestions = ria[16]
        _questionsAsked = ria[17]
        _answersGiven = ria[18]
        _rewards = ria[19]
        _guestIpAddress = ria[20]
        _lastActiveTimeStamp = ria[21]

        m = mongo_utils.get_mongo()
        mongo = m
        return mongo.db.user.insert_one({'uType':_uType, 'userName':_userName, 'password':_password, 'email':_email, 'name':_name,
                                       'birthdate':_birthdate, 'currentLocation':_currentLocation, 'city':_city, 'degree':_degree, 'startDate':_startDate, 'endDate':_endDate,
                                       'companyName':_companyName, 'workExperience':_workExperience, 'interests':_interests, 'languages':_languages,
                                        'photo':_photo, 'savedQuestions':_savedQuestions, 'questionsAsked':_questionsAsked, 'answersGiven':_answersGiven, 
                                        'rewards':_rewards, 'guestIpAddress':_guestIpAddress, 'lastActiveTimeStamp':_lastActiveTimeStamp})