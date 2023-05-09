import os
import datetime as dt

from pydantic import BaseSettings


GPAUTH_SERVICE_BASE_URL = 'https://gp-auth'
GPAUTH_SERVICE_AUTHORIZE_PATH = '/authorize'
GPAUTH_SERVICE_TOKEN_PATH = '/api/v1/token'
GPAUTH_REDIRECT_URI = '/callback'

CLIENT_ID = 'cd5c9ac6-5be9-4926-8ed6-55ea37eb5c37'
CLIENT_SECRET = 'cWAL8LxYLRl9JlFiCNr9qUbGg2xVMX0nhisOTmTJUv5RpzCTvNvFP8ILmUnPV4Z5'

REDIS_DSN = os.environ.get('REDIS_URL')
USER_SESSION_LEN = 64
USER_SESSION_LIFETIME = dt.timedelta(minutes=999)
# USER_SESSION_LIFETIME = dt.timedelta(seconds=10)
USER_SESSION_COOKIE_NAME = 'session'
STATE_LEN = 64
NONCE_LEN = 16