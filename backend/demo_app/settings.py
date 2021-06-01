import os
import sys

from tools.settings import e, boolean_e

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'nruba4s7p#75m^11vnh1*(-zutf-n(04rft41s)oxir*cl_w+j'

TESTING = 'test' in sys.argv or boolean_e('TESTING', False)

if TESTING:
    DEBUG = False
else:
    DEBUG = boolean_e('DEBUG', 1)

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_celery_beat',
    'django_celery_results',
    'celery',

    'asana_crm',
    'users',
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

ROOT_URLCONF = 'demo_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'demo_app.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': e('POSTGRES_DB', 'demo_app'),
        'USER': e('POSTGRES_USER', 'demo_app'),
        'PASSWORD': e('POSTGRES_PASSWORD', 'demo_app'),
        'HOST': e('POSTGRES_HOST', 'database'),
        'PORT': e('POSTGRES_PORT', '5432'),
    }
}


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

AUTH_USER_MODEL = 'users.User'

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = e('STATIC_ROOT', os.path.join(BASE_DIR, "static"))
STATIC_URL = '/static/'

ASANA_ACCESS_TOKEN = e('ASANA_ACCESS_TOKEN', None)

# Celery settings
CELERY_BROKER_URL = e('CELERY_BROKER_URL', 'amqp://guest:guest@rabbitmq/')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TASK_ALWAYS_EAGER = TESTING
CELERY_TASK_EAGER_PROPAGATES = TESTING
CELERY_TIMEZONE = TIME_ZONE
CELERY_ACKS_LATE = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_WORKER_HIJACK_ROOT_LOGGER = False
CELERYD_PREFETCH_MULTIPLIER = 2
CELERYD_MAX_TASKS_PER_CHILD = 1000
CELERY_MAX_RETRIES_COUNT = 5

# Celery-beat settings
MINUTE = 60.0
HOUR = MINUTE * 60
DAY = HOUR * 24

# The interval in seconds between data synchronization with Asana
SYNC_ASANA_INTERVAL = 30

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BEAT_SCHEDULE = {
    'sync_additional_objects_asana': {
        'task': 'asana_crm.tasks.sync_additional_objects',
        'schedule': SYNC_ASANA_INTERVAL,
    },
}

LOG_LEVEL = e('LOG_LEVEL', 'ERROR')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s: %(name)s: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        '': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False
        }
    }
}
