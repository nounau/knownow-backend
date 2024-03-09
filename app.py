from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from src.utils.jwt_helper import jwt
from config import Config


app = Flask(__name__)
load_dotenv('.flaskenv') #the path to your .env file (or any other file of environment variables you want to load)
app.config.from_object(Config)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!

# Register blueprints here

from src.main import bp as main_bp
app.register_blueprint(main_bp)

from src.questions import bp as question_bp
app.register_blueprint(question_bp)

from src.users import bp as user_bp
app.register_blueprint(user_bp)

from src.answers import bp as answer_bp
app.register_blueprint(answer_bp)

from src.authentication import bp as auth_bp
app.register_blueprint(auth_bp)

from src.mailTemplate import bp as mailTemplate_bp
app.register_blueprint(mailTemplate_bp)

jwt.init_app(app)

if __name__ == "__main__":
    app.run()
