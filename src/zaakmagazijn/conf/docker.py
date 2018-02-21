from .base import *

#
# Standard Django settings.
#
ADMINS = ()
MANAGERS = ADMINS

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

#
# Custom settings
#
ENVIRONMENT = 'production'


ZAAKMAGAZIJN_URL = 'http://localhost:8000'

