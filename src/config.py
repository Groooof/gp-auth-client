import os
import datetime as dt

from pydantic import BaseSettings

BASE_URL = 'https://almax-dev.online'
CALLBACK_ROUTE = '/callback'

GPAUTH_SERVICE_BASE_URL = 'https://gp-auth.ru'
GPAUTH_SERVICE_AUTHORIZE_ROUTE = '/authorize'
GPAUTH_SERVICE_TOKEN_ROUTE = '/api/v1/token'

CLIENT_ID = 'e88d30cd-31b0-4b58-b157-6fa6be2f8058'
CLIENT_SECRET = 'OKpIKtRbDE65JhCrZKcJR3nAnuiGZG7uoaDQe4BpknOneTmUHWxgwV6eVWOm2lOR'

REDIS_DSN = os.environ.get('REDIS_URL')
USER_SESSION_LEN = 64
USER_SESSION_LIFETIME = dt.timedelta(minutes=999)
# USER_SESSION_LIFETIME = dt.timedelta(seconds=10)
USER_SESSION_COOKIE_NAME = 'session'
STATE_LEN = 64
NONCE_LEN = 16