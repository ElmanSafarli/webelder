from msal import ConfidentialClientApplication
from django.conf import settings
import requests
import json

client_id = settings.AZURE_CLIENT_ID
client_secret = settings.AZURE_CLIENT_SECRET
tenant_id = settings.AZURE_TENANT_ID

msal_authority = f"https://login.microsoftonline.com/{tenant_id}"

def get_microsoft_graph_access_token():
    
    try:
        url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Access": "application/json",
        }
        
        payload = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "https://graph.microsoft.com/.default",
        }

        response = requests.post(url=url, headers=headers, data=payload)
        responce_data = response.json()
        access_token = responce_data["access_token"]
        # print(access_token)
        return access_token
    except:
        return None


def read_email(request):
    access_token = get_microsoft_graph_access_token()

    # print(request)

    if access_token:
        url = f"https://graph.microsoft.com/v1.0/users?$filter=userPrincipalName eq '{request.user.email}'"

        headers = {
            "Authorization": 'Bearer ' + access_token,
            "Content-Type": "application/json",
        }

        response = requests.get(url=url, headers=headers)
        json_responce = response.json()

        # print(json_responce)
        return json_responce


