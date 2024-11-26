import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()


GOOGLE_OAUTH_CLIENT_ID = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
if not GOOGLE_OAUTH_CLIENT_ID:
    raise ValueError(
        'GOOGLE_OAUTH_CLIENT_ID is missing.' 
        'Have you put it in a file at core/.env ?'
    )

# We need these lines below to allow the Google sign in popup to work.
SECURE_REFERRER_POLICY = 'no-referrer-when-downgrade'
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ALLOWED_HOSTS = ['*']


import environ

env = environ.Env()
environ.Env.read_env()  # This reads the .env file

# Access variables
API_KEY = env("API_KEY", default="api_key")
DOMAIN = env("DOMAIN", default="domain")
FROM = env("FROM", default="from")