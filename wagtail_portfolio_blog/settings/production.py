from __future__ import absolute_import, unicode_literals

from wagtail_portfolio_blog.settings.dev import SECRET_KEY
from .base import *
import dj_database_url
from decouple import config

SECRET_KEY = config('SECRET_KEY')

DEBUG = False

DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOST = ['*']

try:
    from .local import *
except ImportError:
    pass
