from .base import *

DEBUG = False
ALLOWED_HOSTS = ["https://quizweb258-846e7e38a412.herokuapp.com/"]

import django_heroku
import dj_database_url

DATABASES = {"default": dj_database_url.config(conn_max_age=600)}

django_heroku.settings(locals())
