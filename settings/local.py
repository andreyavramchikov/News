from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'news',
        'USER': 'root',
        'PASSWORD': 'andreyPasan1',
        'HOST': 'news.csm5tqswx2ek.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
    }
}