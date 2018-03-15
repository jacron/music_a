"""
Django settings for music project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!=8kkm995y^8)_*=_0#x_1xby*@651)zi+)ccj%b6s^03$)ui_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'website',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'music.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + 'website/templates/',
            BASE_DIR + 'website/templatetags/'
        ],
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

WSGI_APPLICATION = 'music.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join('static'),)

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('localhost', 6379)],
        },
        'ROUTING': 'music.routing.channel_routing',
    }
}

MEDIA_PLAYER = '/Applications/Media Center 21.app'
TAG_EDITOR = '/Applications/Tag Editor.app'
SQLITE3_FILE = '/Users/orion/db/db.music.sqlite3'
COVER_FILE = '/folder.jpg'
BACK_FILE = '/back.jpg'
PERSON_FILE = 'person.jpg'
INSTRUMENTS_PATH = '/Volumes/Media/Audio/Klassiek/Instrumenten/'
COMPONIST_PATH = '/Volumes/Media/Audio/Klassiek/Componisten/'
PERFORMER_PATH = '/Volumes/Media/Audio/Klassiek/Performers/'
LIBRARYCODE_PATH = '/Volumes/Media/Audio/Klassiek/LibraryCode/'
COVER_PATH = '/Volumes/Media/tmpscan/{}.jpg'
SCORE_FRAGMENT_PATH = '/Volumes/Media/Audio/Klassiek/LibraryCode/{}.png'
PYTHON_3_PATH = '/Users/orion/anaconda/bin/python'

TMP_PATH = '/Volumes/Media/tmpscan'
SKIP_DIRS = ['website', 'websites', 'artwork', 'Artwork', 'etc', 'scans',
             'Scans', 'scan',
             'website boxset', '#Booklets', 'Pixels', 'Graphics', 'Info + Art',
             'Art', 'Covers', ]
MUSIC_FILES = ('cue', "flac", "ape", "mp3", "iso", "wma", "wav", "mp3", "m4a",
               'dsf', 'dff')
NOT_FOUND_IMAGE_PATH = '/Volumes/Media/Audio/Klassiek/empty/notfound.jpg'
SAVECLIP_PATH = '/Users/orion/scripts/saveclip.py'
