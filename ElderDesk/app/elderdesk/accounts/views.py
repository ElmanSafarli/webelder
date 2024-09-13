from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from requests_oauthlib import OAuth2Session
from django.urls import reverse
import requests
import json
import logging

logger = logging.getLogger(__name__)

# Helper function to get access token
def get_access_token():
    url = f"{settings.AZURE_AUTHORITY}/oauth2/v2.0/token"
    data = {
        'grant_type': 'client_credentials',
        'client_id': settings.AZURE_CLIENT_ID,
        'client_secret': settings.AZURE_CLIENT_SECRET,
        'scope': 'https://graph.microsoft.com/.default',
    }
    
    response = requests.post(url, data=data)
    response.raise_for_status()
    token_json = response.json()
    return token_json.get('access_token')


# View to handle Outlook login and redirect to Microsoft for OAuth
def outlook_login_view(request):
    # OAuth2 session with the client ID and redirect URI
    outlook = OAuth2Session(settings.AZURE_CLIENT_ID, redirect_uri=settings.AZURE_REDIRECT_URI)
    
    authorization_url, state = outlook.authorization_url(f"{settings.AZURE_AUTHORITY}/oauth2/v2.0/authorize", prompt='login')
    
    # Save the state in the session to validate against the callback
    request.session['oauth_state'] = state
    
    return redirect(authorization_url)


# View to handle the callback from Microsoft Azure after login
def outlook_callback_view(request):
    outlook = OAuth2Session(settings.AZURE_CLIENT_ID, redirect_uri=settings.AZURE_REDIRECT_URI, state=request.session['oauth_state'])
    
    # Exchange the authorization code for an access token
    token = outlook.fetch_token(
        f"{settings.AZURE_AUTHORITY}/oauth2/v2.0/token",
        client_secret=settings.AZURE_CLIENT_SECRET,
        authorization_response=request.build_absolute_uri()
    )
    
    # Use the token to fetch user info from Microsoft Graph
    user_info = get_user_info(token)
    
    if user_info:
        # Check if the user exists in your system; if not, create the user (registration)
        user = authenticate_and_register(user_info)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))  # Redirect to dashboard or home page
        else:
            return render(request, 'account/login_failed.html', {'error': 'Failed to authenticate or register the user.'})
    else:
        return render(request, 'account/login_failed.html', {'error': 'Failed to fetch user information from Microsoft.'})


# Fetch user information from Microsoft Graph
def get_user_info(token):
    graph_url = 'https://graph.microsoft.com/v1.0/me'
    headers = {
        'Authorization': f'Bearer {token["access_token"]}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(graph_url, headers=headers)
        response.raise_for_status()
        user_info = response.json()
        return user_info
    except requests.RequestException as e:
        logger.error(f"Failed to fetch user info: {e}")
        return None


# Function to authenticate the user or register them if they don't exist
def authenticate_and_register(user_info):
    email = user_info['mail'] or user_info['userPrincipalName']
    first_name = user_info.get('givenName', '')
    last_name = user_info.get('surname', '')

    try:
        # Try to get the user by their email
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Register the user if they don't exist
        user = User(username=email, email=email, first_name=first_name, last_name=last_name)
        user.set_unusable_password()  # Since password is managed via OAuth
        user.save()

    return user
