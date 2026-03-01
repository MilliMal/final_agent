from flask import Flask, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
flask_app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(flask_app)
CORS(flask_app)

# Initialize session
from flask_session import Session
Session(flask_app)

# Import models
from models import User

# Import routes
from routes.auth import auth_bp
from routes.slack import slack_bp

flask_app.register_blueprint(auth_bp)
flask_app.register_blueprint(slack_bp)

@flask_app.route('/')
def index():
    return {'message': 'Agent API is running'}

if __name__ == '__main__':
    with flask_app.app_context():
        db.create_all()
    flask_app.run(debug=os.getenv('FLASK_DEBUG', False), port=int(os.getenv('PORT', 5000)))
