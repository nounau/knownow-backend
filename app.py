from app import create_app
from dotenv import load_dotenv

app = create_app()
load_dotenv('.flaskenv') #the path to your .env file (or any other file of environment variables you want to load)

if __name__ == "__main__":
    app.run()
