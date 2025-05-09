# encoding: utf-8

from jpl.labcas.dicominator.policy.settings.dev import *  # noqa: F401, F403
from django.conf import global_settings

SECRET_KEY = '⚠️ insecure — do not use ⚠️'
ALLOWED_HOSTS = ['*']  # Do not use, for local dev only


CACHES = globals().get('CACHES', global_settings.CACHES)
for cache, settings in CACHES.items():
    options = settings.get('OPTIONS', {})
    options['TIMEOUT'] = 0


# Silence other checks here in the future:
# SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']
