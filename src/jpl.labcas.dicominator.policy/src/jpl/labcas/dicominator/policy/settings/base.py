# encoding: utf-8

'''📜 Dicominator site policy's base settings.'''

from .ldap import *  # noqa: F401, F403
import dj_database_url, os
import jpl.labcas.dicominator.content.settings as content_settings
import jpl.labcas.dicominator.theme.settings as theme_settings
import jpl.labcas.dicominator.tags.settings as tags_settings


# Installed Applications
# ----------------------
#
# The "apps" (Python packages) enabled for Django.
#
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps


INSTALLED_APPS = content_settings.INSTALLED_APPS + tags_settings.INSTALLED_APPS + theme_settings.INSTALLED_APPS + [
    'jpl.labcas.dicominator.content',
    'jpl.labcas.dicominator.theme',
    'jpl.labcas.dicominator.tags',

    # Menus
    'wagtail.contrib.modeladmin',
    'wagtailmenus',

    # Wagtail:
    'wagtail.contrib.redirects',
    'wagtail.contrib.settings',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',
    'taggit',
    'modelcluster',

    # Django:
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Add-ons, for the future if needed:
    # 'django_celery_results',

    # This Is Us™:
    'jpl.labcas.dicominator.policy',
]


# Migration Modules
# -----------------
#
# This shouldn't be necessary, but I am seeing the generated migrations code end up in the virtual
# environment and not in the source tree when running `make migrations` 🤨
#
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules

MIGRATION_MODULES = {
    'jpl.labcas.dicominator.policy': 'jpl.labcas.dicominator.policy.migrations',
    **content_settings.MIGRATION_MODULES,
    **theme_settings.MIGRATION_MODULES,
    **tags_settings.MIGRATION_MODULES,
}


# Middleware
# ----------
#
# Pipeline processors on the request/response.
#
# 🔗 https://docs.djangoproject.com/en/dev/topics/http/middleware/

MIDDLEWARE = [
    # Django:
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Wagtail:
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]


# Root URL Configuration
# ----------------------
#
# Name of the module that contains URL patterns.
#
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf

ROOT_URLCONF = 'jpl.labcas.dicominator.policy.urls'


# Templates
# ---------
#
# The template engines and getting them going, etc.
#
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#templates

TEMPLATES = theme_settings.TEMPLATES + [
    {
        'NAME': 'jpl.labcas.dicominator.policy',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtail.contrib.settings.context_processors.settings',  # For global settings
            ],
        },
    },
]


# Application for Web Services Gateway Interface
# ----------------------------------------------
#
# Full path to Python object that's the WSGI application.
#
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application

WSGI_APPLICATION = 'jpl.labcas.dicominator.policy.wsgi.application'


# Type of Primary Key Field for Models
# ------------------------------------
#
# For models that don't have a primary key field, they get a default. This tells the data type
# of that field, `BigAutoField` in this case.
#
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Internationalization
# --------------------
#
# Settings for time zones, languages, locales, etc.
#
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#language-code
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TIME_ZONE
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-USE_I18N
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-USE_L10N
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-USE_TZ

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_L10N      = True
USE_TZ        = True


# Databases
# ---------
#
# We let the magic of `dj-database-url` set this up for us. Note that `DATABASE_URL` will need to be
# provided in the environment.
#
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#databases
# 🔗 https://pypi.org/project/dj-database-url/

DATABASES = {'default': dj_database_url.config(default='postgresql://:@/dicominator', conn_max_age=120)}  # seconds


# Password Strength
# -----------------
#
# We don't use this because users keep creds in LDAP
#
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []


# Site Identification
# -------------------
#
# 🔗 https://docs.wagtail.io/en/stable/reference/settings.html#wagtail-site-name

WAGTAIL_SITE_NAME = 'Dicominator'


# Admin Base URL
# --------------
#
# 🔗 https://docs.wagtail.org/en/stable/reference/settings.html#wagtailadmin-base-url
#
# 🔮 TODO what should I put here?

WAGTAILADMIN_BASE_URL = os.getenv('BASE_URL', 'https://edrn-labcas.jpl.nasa.gov/dicominator/')


# Static Files and Media
# ----------------------
#
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-STATIC_URL
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-STATIC_ROOT
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#media-root
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#media-url

STATIC_URL = os.getenv('STATIC_URL', '/static/')
MEDIA_URL = os.getenv('MEDIA_URL', '/media/')
STATIC_ROOT = os.getenv('STATIC_ROOT', os.path.join(os.path.abspath(os.getcwd()), 'static'))
MEDIA_ROOT = os.getenv('MEDIA_ROOT', os.path.join(os.path.abspath(os.getcwd()), 'media'))


# HTTP Subpath Support
# --------------------
#
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FORCE_SCRIPT_NAME

fsn = os.getenv('FORCE_SCRIPT_NAME')
if fsn is not None: FORCE_SCRIPT_NAME = fsn


# Search
# ------
#
# 🔗 https://docs.wagtail.org/en/stable/reference/settings.html#wagtailsearch-backends
#
# 🔮 TODO: may not even need this as no "real" content is expected

WAGTAILSEARCH_BACKENDS = {
    'default': {'BACKEND': 'wagtail.search.backends.database'}
}


# Caching
# -------
#
# Note that in Django dev Memcached is supported, and in 4.0 Redis becomes supported.
#
# Update: we're now on Django 4.0, however the cache support is rudimentary. We'll stick with
# `django_redis` for now.
#
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#caches
# 🔗 https://github.com/jazzband/django-redis
 

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    # If necessary, we can define better caches, and additional caches such as a renditions cache
}


# CSRF
#
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#csrf-trusted-origins

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'http://*.jpl.nasa.gov,https://*.jpl.nasa.gov').split(',')


# Logging
# -------
#
# There's got to be a better way to set this up tersely without clobbering existing settings while
# still be resilient in the face of no settings 😬
#
# 🔗 https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-LOGGING

from django.utils.log import DEFAULT_LOGGING  # noqa
LOGGING = globals().get('LOGGING', DEFAULT_LOGGING)
loggers = LOGGING.get('loggers', {})
eke_knowledge = loggers.get('jpl.labcas.dicominator', {})
eke_knowledge_handlers = set(eke_knowledge.get('handlers', []))
eke_knowledge_level = eke_knowledge.get('level', 'INFO')
eke_knowledge_handlers.add('console')
eke_knowledge['handlers'] = list(eke_knowledge_handlers)
eke_knowledge['level'] = eke_knowledge_level
loggers['jpl.labcas.dicominator'] = eke_knowledge
