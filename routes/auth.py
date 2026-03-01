from flask import Blueprint, request, session, jsonify, redirect, url_for
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
from app import db
from models import User
from utils.google_auth import get_user_info

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

SCOPES = [
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/drive'
]

@auth_bp.route('/google')
def google_auth():
    """Initiate Google OAuth flow"""
    flow = Flow.from_client_secrets_file(
        'credentials.json',
        scopes=SCOPES,
        redirect_uri=os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:5000/auth/google/callback')
    )
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)

@auth_bp.route('/google/callback')
def google_callback():
    """Handle Google OAuth callback"""
    state = session.get('state')
    flow = Flow.from_client_secrets_file(
        'credentials.json',
        scopes=SCOPES,
        state=state,
        redirect_uri=os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:5000/auth/google/callback')
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    
    user_info = get_user_info(credentials)
    
    user = User.query.filter_by(google_id=user_info['id']).first()
    if not user:
        user = User(
            google_id=user_info['id'],
            email=user_info['email'],
            name=user_info.get('name'),
            profile_picture=user_info.get('picture')
        )
        db.session.add(user)
    
    user.access_token = credentials.token
    user.refresh_token = credentials.refresh_token
    db.session.commit()
    
    session['user_id'] = user.id
    return redirect(os.getenv('FRONTEND_URL', 'http://localhost:3000'))

@auth_bp.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'message': 'Logged out successfully'})

@auth_bp.route('/me')
def get_current_user():
    """Get current authenticated user"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'profile_picture': user.profile_picture
    })
