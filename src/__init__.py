# # Inside app/__init__.py

# from flask import Flask
# from flask_jwt_extended import JWTManager
# from app.utils.jwt_helper import jwt
# from config import Config

# def create_app(config_class=Config):
#     app = Flask(__name__)
#     app.config.from_object(config_class)

#     app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!

#     # Register blueprints here

#     from app.main import bp as main_bp
#     app.register_blueprint(main_bp)

#     from app.questions import bp as question_bp
#     app.register_blueprint(question_bp)

#     from app.users import bp as user_bp
#     app.register_blueprint(user_bp)

#     from app.answers import bp as answer_bp
#     app.register_blueprint(answer_bp)

#     from app.authentication import bp as auth_bp
#     app.register_blueprint(auth_bp)

#     from app.mailTemplate import bp as mailTemplate_bp
#     app.register_blueprint(mailTemplate_bp)

#     jwt.init_app(app)

#     return app
