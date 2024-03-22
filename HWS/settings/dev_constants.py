from .common_constants import *

BASE_URI = BASE_DEV_URI

GOOGLE_CLIENT_ID = ""
GOOGLE_CLIENT_SECRET = ""

GOOGLE_REDIRECT_URI = f"{BASE_URI}/accounts/google/login/callback/"

GOOGLE_LOGIN_REDIRECT_URI = (
        f"{BASE_GOOGLE_URL}"
        f"response_type={'code'}"
        f"&scope={GOOGLE_SCOPES}"
        f"&access_type={'online'}"
        f"&include_grant_scopes={'true'}"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
    )
