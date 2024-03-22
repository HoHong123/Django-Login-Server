from pathlib import Path
from datetime import timedelta
from django.utils import timezone

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
        'API.authentication.CustomJWTAuthentication',
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
    "TOKEN_OBTAIN_SERIALIZER": "API.serializers.CustomTokenObtainPairSerializer", # 
}


# ==========================================================
# Logger 설정
BASE_LOGGER = 'hitup.prod'

ADMINS = [
    ('GIBEON','gibeonsoftware@gmail.com'),
    ('PKH','epzmhs@gmail.com'),
    ('JUN','twszak02@gmail.com'),
    ]

# 로깅설정
LOGGING = {
    # logging 모듈이 업그레이드되어도 현재 설정을 보장해 주는 안전장치
    'version': 1,
    # 디폴트 : True, 장고의 디폴트 로그 설정을 대체.
    #         False, 장고의 디폴트 로그 설정의 전부 또는 일부를 다시 정의
    'disable_existing_loggers': False,
    'filters': {                    # 특정 조건에서 로그를 출력하거나 출력하지 않기 위해서 사용
        'require_debug_false': {    # DEBUG=False이면 사용하는 필터
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {     # DEBUG=True이면 사용하는 필터
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # 로그 출력 포맷 설정
    'formatters': {
        'hitup_dev': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
        'standard': {
            # [시간][레벨]::이름 = 메시지
            'format': '[%(asctime)s][%(levelname)s]::%(name)s = %(message)s'
        },
    },
    # 출력 방법 설정
    'handlers': {
        # DEBUG 이상, DEBUG=True 일때 로그 출력
        'console': {                                        # 콘솔 핸들러
            'level': 'DEBUG',                               # DEBUG 이상 레벨
            'filters': ['require_debug_true'],              # DEBUG=True인 경우
            'class': 'logging.StreamHandler',               # logging.StreamHandler 데이터 출력
            'formatter': 'hitup_dev',                 # hitup_runserver 포맷 사용
        },
        # runserver 개발 서버에서 로그를 출력
        'hitup_dev': {                                # 장고 서버 핸들러
            'level': 'INFO',                                # INFO 이상 레벨
            'class': 'logging.StreamHandler',               # logging.StreamHandler 데이터 출력
            'formatter': 'hitup_dev',                 # hitup_runserver 포맷 사용
        },
        # ADMINS에 설정된 이메일로 DEBUG=false, ERROR 이상 메시지 전송 (Require SMTP)
        'mail_admins': {                                    # 어드민 이메일 핸들러
            'level': 'ERROR',                               # 에러 이상 메시지 핸들링
            'filters': ['require_debug_false'],             # 디버그가 불가능할 경우
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {                                           # 파일 저장 핸들러
            'level': 'INFO',                                # INFO 이상 레벨
            'filters': ['require_debug_false'],             # 디버그가 불가능할 경우
            'class': 'logging.handlers.RotatingFileHandler',# 파일 저장 디렉토리
            # 파일 저장 경로 및 파일명 선택
            'filename': BASE_DIR / timezone.now().strftime('Logs/HitupHistory_Prod_%Y.%m.%d_%HH.log'), 
            'maxBytes': 1024*1024*5,  # 5 MB                # 파일 최대 크기 설정
            'backupCount': 5,                               # 롤링되는 파일의 개수, 총 5개의 로그 파일로 유지되도록 설정
            'encoding' : 'utf-8',                           # 한글 적용을 위한 utf-8 인코딩 값 입력
            'formatter': 'standard',                        # 저장 문자 포맷 설정
        },
        'file_dev': {                                 # 파일 저장 핸들러
            'level': 'INFO',                                # INFO 이상 레벨
            'filters': ['require_debug_true'],            # 디버그가 불가능할 경우
            'class': 'logging.handlers.RotatingFileHandler',# 파일 저장 디렉토리
            # 파일 저장 경로 및 파일명 선택
            'filename': BASE_DIR / timezone.now().strftime('Logs/HitupHistory_Dev_%Y.%m.%d_%HH.log'),
            'maxBytes': 1024*1024*5,  # 5 MB                # 파일 최대 크기 설정
            'backupCount': 5,                               # 롤링되는 파일의 개수, 총 5개의 로그 파일로 유지되도록 설정
            'encoding' : 'utf-8',                           # 한글 적용을 위한 utf-8 인코딩 값 입력
            'formatter': 'standard',                        # 저장 문자 포맷 설정
        },
    },
    'loggers': {
        'debugger': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'hitup': {
            'handlers': ['mail_admins'],
            'level': 'INFO',
        },
        'hitup.prod': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'hitup.dev': {
            'handlers': ['hitup_dev', 'file_dev'],
            'level': 'INFO',
            'propagate': False, # 상위 계층에 전달 여부
        },
    }
}