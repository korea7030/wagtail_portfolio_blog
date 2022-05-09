from __future__ import absolute_import, unicode_literals

from .base import *
import dj_database_url
from decouple import config

# SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = True

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

try:
    from .local import *
except ImportError:
    pass
