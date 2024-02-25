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

    from app.todo import bp as todo_bp
    app.register_blueprint(todo_bp)


    return app