from src.modules.authentication.models.auth_data import auth_data

class auth_service:

    @staticmethod
    def authenticate(email, password):
        return auth_data.authenticate(email, password)
    
    @staticmethod
    def register(register_info_array):
        return auth_data.register(register_info_array)