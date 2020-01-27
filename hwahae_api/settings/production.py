import os
from django.db.backends.mysql.base import DatabaseWrapper
from .base import *

DatabaseWrapper.data_types["DateTimeField"] = "datetime"  # fix for MySQL 5.5

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": os.environ["MYSQL_ROOT_HOST"],
        "NAME": os.environ["MYSQL_DATABASE"],
        "USER": os.environ["MYSQL_USER"],
        "PASSWORD": os.environ["MYSQL_ROOT_PASSWORD"],
    }
}
