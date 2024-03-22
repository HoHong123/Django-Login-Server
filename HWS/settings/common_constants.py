"""
you can use constants with djang.conf.settings

for example : 
from django.conf import settings

print(settings.MY_CONSTANT)
"""
BASE_PROD_URI = 'https://'
BASE_DEV_URI = 'http://'
BASE_LOCAL_URI = 'http://'

BASE_TOKEN_URI = 'https://oauth2.googleapis.com/token'
BASE_GOOGLE_URL = "https://accounts.google.com/o/oauth2/v2/auth?"

GOOGLE_SCOPES = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
