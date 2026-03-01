from flask import Flask, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)
CORS(app)

# Initialize session
from flask_session import Session
Session(app)

# Import models
from models import User

# Import routes
from routes.auth import auth_bp
from routes.slack import slack_bp

app.register_blueprint(auth_bp)
app.register_blueprint(slack_bp)

@app.route('/')
def index():
    return {'message': 'Agent API is running'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=os.getenv('FLASK_DEBUG', False), port=int(os.getenv('PORT', 5000)))
