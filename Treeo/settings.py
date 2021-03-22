"""
Django settings for Treeo project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@ve)bkx%=)lze7xivvbo-0ec(&)=t6k+jse%d8f2bkq+!+j56s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

from .email_info import *
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT
#EMAIL_BACKEND = EMAIL_BACKEND
# Application definition

INSTALLED_APPS = [
    'apptArchive.apps.ApptarchiveConfig',
    'patient_log.apps.PatientLogConfig',
    'users_acc.apps.UsersAccConfig',
    'ReqAppt.apps.ReqapptConfig',
    'messaging.apps.MessagingConfig',
    'upload_download.apps.UploadDownloadConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chartjs',
    # 'channels',
    'phonenumber_field',
    'blogsys.apps.BlogsysConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users_acc.middleware.SessionTimeoutMiddleware',
]

ROOT_URLCONF = 'Treeo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.joinpath('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Treeo.wsgi.application'
# ASGI_APPLICATION = 'Treeo.routing.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'treeohealthdb',
        'USER': 'root',
        'PASSWORD': 'M!ddle1*',
        'HOST': '127.0.0.1',  # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        # 'ENGINE': 'mysql.connector.django',
        # 'NAME': 'treeohealthdb',
        # 'USER': 'treeo_master@treeo-server',
        # 'PASSWORD': 'Password1',
        # 'HOST': 'treeo-server.mysql.database.azure.com',  # Or an IP Address that your DB is hosted on
        # 'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
#when you close the browser it doesnt log you out
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#your session are closed out after 5min 300 sec
SESSION_COOKIE_AGE = 3000
SESSION_SAVE_EVERY_REQUEST = True
#restricted to us phone numbers as default can store international under e164 standard but no tests with other country codes
PHONENUMBER_DB_FORMAT ='E164'
PHONENUMBER_DEFAULT_REGION = 'US'
PHONENUMBER_DEFAULT_FORMAT ='NATIONAL'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


STATIC_URL = '/static/'
AUTH_USER_MODEL = 'users_acc.User'
STATICFILES_DIRS = [BASE_DIR.joinpath('static')]


#LOGIN_REDIRECT_URL='home'
LOGIN_URL='login'
MEDIA_ROOT= (BASE_DIR.joinpath('static'))
MEDIA_URL='media/'