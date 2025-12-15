from .base import *

DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT", "5432"),
    }
}


import os
from dotenv import load_dotenv
load_dotenv()

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")


STATIC_ROOT = BASE_DIR / "staticfiles"

#client API settings for production
CLIENT_API_TOKEN = os.getenv("CLIENT_API_TOKEN")

CLIENT_CITY_API_URL = os.getenv("CLIENT_CITY_API_URL")
CLIENT_TEST_API_URL = os.getenv("CLIENT_TEST_API_URL")
CLIENT_DIAGNOSTIC_API_URL = os.getenv("CLIENT_DIAGNOSTIC_API_URL")
CLIENT_VISIT_TYPE_API_URL = os.getenv("CLIENT_VISIT_TYPE_API_URL")
CLIENT_HEALTH_PACKAGE_API_URL = os.getenv("CLIENT_HEALTH_PACKAGE_API_URL")
CLIENT_SPONSORED_PACKAGE_API_URL = os.getenv("CLIENT_SPONSORED_PACKAGE_API_URL")


CLIENT_DOCTORSPECIALITY_API_URL=os.getenv("CLIENT_DOCTORSPECIALITY_API_URL",None)
CLIENT_LANGUAGE_API_URL=os.getenv("CLIENT_LANGUAGE_API_URL",None)
CLIENT_PINCODE_API_URL=os.getenv("CLIENT_PINCODE_API_URL",None)
CLIENT_DOCTOR_URL=os.getenv("CLIENT_DOCTOR_URL",None)
CLIENT_VENDOR_URL=os.getenv("CLIENT_VENDOR_URL",None)
