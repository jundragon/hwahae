import os
from .base import *

DEBUG = True

if DEBUG:
    # Database
    # https://docs.djangoproject.com/en/2.1/ref/settings/#databases

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "HOST": "127.0.0.1",
            "NAME": "hwahae_db",
            "USER": "root",
            "PASSWORD": "password",
        }
    }

# if DEBUG:

#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#         }
#     }
