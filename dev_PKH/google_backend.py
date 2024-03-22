from django.contrib.auth.backends import BaseBackend
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest

from django.conf import settings
from dev_JUN.views import *

import requests


class GoogleAuthBackend(BaseBackend):
    """Custom Backend Server for Google auth """
    def _getAccessToken(self, code):
        response = requests.post(
            settings.BASE_TOKEN_URI,
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                'client_secret': settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            }
        )
        return response.json()

    """
    Authentication function for Custom google token verification
    parms:
        code - Google code received form view
    """
    def authenticate(self, request, code=None):
        if code:
            token = self._getAccessToken(code)
            
            #id_token = token.get('id_token')
            accessToken = token.get('access_token')
            
            if accessToken:
                googleUserDetails = requests.get(f'https://www.googleapis.com/oauth2/v2/userinfo?access_token={accessToken}')
                return googleUserDetails.json()
            else:
                return None
