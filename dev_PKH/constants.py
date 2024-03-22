GOOGLE_CLIENT_ID = ""
GOOGLE_CLIENT_SECRET = ""

BASE_URI = 'http://'

BASE_GOOGLE_URL = "https://accounts.google.com/o/oauth2/v2/auth?"

GOOGLE_REDIRECT_URI = f"{BASE_URI}/accounts/google/login/callback/"

GOOGLE_SCOPES = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"

GOOGLE_LOGIN_REDIRECT_URI = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"response_type={'code'}"
        f"&scope={GOOGLE_SCOPES}"
        f"&access_type={'online'}"
        f"&include_grant_scopes={'true'}"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
    )
