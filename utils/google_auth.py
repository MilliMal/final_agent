"""Google Authentication Utilities"""
import requests
from google.auth.transport.requests import Request

def get_user_info(credentials):
    """
    Fetch user information from Google API
    
    Args:
        credentials: Google OAuth credentials
        
    Returns:
        dict: User information including id, email, name, picture
    """
    url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    headers = {'Authorization': f'Bearer {credentials.token}'}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json()

def refresh_credentials(credentials):
    """
    Refresh Google OAuth credentials
    
    Args:
        credentials: Google OAuth credentials
        
    Returns:
        Credentials: Refreshed credentials
    """
    if credentials.expired:
        request = Request()
        credentials.refresh(request)
    
    return credentials

def revoke_credentials(access_token):
    """
    Revoke Google OAuth credentials
    
    Args:
        access_token: Google access token to revoke
    """
    url = 'https://oauth2.googleapis.com/revoke'
    params = {'token': access_token}
    
    requests.post(url, params=params)
