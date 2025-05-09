# encoding: utf-8

'''📜 Site policy.'''

# If we ever need async tasks:
# from .celery import app as celery_app

import importlib.resources


PACKAGE_NAME = __name__
__version__ = VERSION = importlib.resources.files(__name__).joinpath('VERSION.txt').read_text().strip()


__all__ = (
    # If we ever need async tasks:
    # celery_app,
    PACKAGE_NAME,
    VERSION,
)
