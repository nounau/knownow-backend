from flask import Flask

from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register blueprints here

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.questions import bp as question_bp
    app.register_blueprint(question_bp)

    from app.users import bp as user_bp
    app.register_blueprint(user_bp)

    from app.answers import bp as answer_bp
    app.register_blueprint(answer_bp)

    return app