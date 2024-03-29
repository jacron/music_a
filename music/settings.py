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

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    '10.0.1.6',
    '0.0.0.0',
    '127.0.0.1',
    'localhost',
)
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
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
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

MEDIA_PLAYER = '/Applications/Media Center 24.app'
MEDIA_PLAYER_APP = 'Media Center 24'
TAG_EDITOR = '/Applications/Tag Editor.app'
COVER_FILE = '/folder.jpg'
BACK_FILE = '/back.jpg'
PERSON_FILE = 'person.jpg'
PYTHON_3_PATH = '/Users/orion/anaconda/bin/python'
SAVECLIP_PATH = '/Users/orion/scripts/saveclip.py'
BR_API_URL = 'https://api.buienradar.nl/image/1.0/RadarMapNL?'

MUSIC_PATHS = {
    'abeel': {
        'AUDIO_ROOT': '/Volumes/Abeel/',
        'SQLITE3_FILE': '/Users/orion/db/db.abeel.sqlite',
    },
    'saturnus': {
        'AUDIO_ROOT': '/Volumes/Media/Audio/Klassiek/',
        'SQLITE3_FILE': '/Users/orion/db/db.music.sqlite3',
    },
    'windows': {
        'AUDIO_ROOT': 'E:/',
        'SQLITE3_FILE': 'E:/db/db.abeel.sqlite',
    },
}
# config paths here, choosing 'abeel', 'saturnus' or 'windows'
# SOURCE = 'abeel'  # sdd disk in iMac or macBook
# SOURCE = 'windows'  # sdd disk in Dell
SOURCE = 'saturnus'  # iMac or macBook
AUDIO_ROOT = MUSIC_PATHS[SOURCE]['AUDIO_ROOT']
SQLITE3_FILE = MUSIC_PATHS[SOURCE]['SQLITE3_FILE']

INSTRUMENTS_PATH = AUDIO_ROOT + 'Instrumenten'
COMPONIST_PATH = AUDIO_ROOT + 'Componisten/'
PERFORMER_PATH = AUDIO_ROOT + 'Performers/'
LIBRARYCODE_PATH = AUDIO_ROOT + 'LibraryCode/'
SCORE_FRAGMENT_PATH = AUDIO_ROOT + 'LibraryCode/{}.png'
TMP_PATH = AUDIO_ROOT + 'tmpscan'
COVER_PATH = AUDIO_ROOT + 'tmpscan/{}.jpg'
NOT_FOUND_IMAGE_PATH = AUDIO_ROOT + 'empty/notfound.jpg'

SKIP_DIRS = ['website', 'websites', 'artwork', 'Artwork', 'etc', 'scans',
             'Scans', 'scan', 'covers',
             'website boxset', '#Booklets', 'Pixels', 'Graphics', 'Info + Art',
             'Art', 'Covers', 'boxset_files', ]
MUSIC_FILES = ('cue', "flac", "ape", "mp3", "iso", "wma", "wav", "mp3", "m4a",
               'dsf', 'dff')
INTERESTING_METATAGS = [
    'performer', 'totaltracks', 'title', 'album', 'albumartist', 'artist',
    'composer', 'comment', 'date', 'year', 'totaldiscs', 'discid'
]