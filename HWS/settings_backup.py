from pathlib import Path
from datetime import timedelta
import pymysql
pymysql.install_as_MySQLdb()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ql67mm5sp=f!(^zl4df5)mo9r(2p+p%75(fmx!z=^4cdu4-p9t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 접근 가능한 호스트
ALLOWED_HOSTS = ['*']

# Application definition
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django.contrib.sites', # 장고 site 앱
    
    'rest_framework', # rest api 용
    
    # Add django-allauth package app informations
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    # 소셜로그인 제공자 리스트
    'allauth.socialaccount.providers.naver',  
    'allauth.socialaccount.providers.kakao',  
    'allauth.socialaccount.providers.google',
]

CUSTOM_APPS = [
    # Add common app
    'API',
    'common', # 공통 사용 함수, 변수들을 위한 앱 추가
    
    # Add PKH app
    'dev_PKH',
    
    # 정준이 작업용 앱
    'dev_JUN', 
]

INSTALLED_APPS =  DEFAULT_APPS + CUSTOM_APPS

MIDDLEWARE = [
    # Add middleware for allauth
    'allauth.account.middleware.AccountMiddleware',
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware', # CSRF 검증 생략
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'HWS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR/'templates',
            ], # updated line
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                # 'allauth' requirement
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'HWS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER' : 'test',
        'PASSWORD' : '1234', # 설정한 비밀번호로 적어주면 된다.
        'HOST' : '192.168.0.118',
        'PORT' : '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==========================================================
# Google OAUTH 2.0 properties
# Init : 24.02.08 PKH

# Require for google sign-in
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    'allauth.account.auth_backends.AuthenticationBackend'
]


# ==========================================================
# Rest FRAMEWORK 설정
REST_FRAMEWORK = { # 권한 설정
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'dev_JUN.authentication.CustomJWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.permissions.IsAuthenticated', # 인증된 사용자만 접근 가능
    ],
}

# JWT 설정
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None, 
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'uid',
    'USER_ID_CLAIM': 'uid',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    "TOKEN_OBTAIN_SERIALIZER": "dev_JUN.serializers.CustomTokenObtainPairSerializer", # 
}
