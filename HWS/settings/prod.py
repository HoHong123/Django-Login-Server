from .base import *
from .prod_constants import *

DEBUG = False

ALLOWED_HOSTS = ['hitup.shop']

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hitup',
        'USER' : 'deployer',
        'PASSWORD' : '1234', # 설정한 비밀번호로 적어주면 된다.
        'HOST' : '127.0.0.1',
        'PORT' : '3306',
    }
}
