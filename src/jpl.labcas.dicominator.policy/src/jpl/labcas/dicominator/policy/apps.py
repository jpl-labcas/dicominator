# encoding: utf-8

'''📜 Site policy: Django apps config.'''

from django.apps import AppConfig


class DicominatorPolicyConfig(AppConfig):
    '''The Dicominator policy app.'''
    name = 'jpl.labcas.dicominator.policy'
    label = 'jpllabcasdicominatorpolicy'
    verbose_name = 'Dicominator Policy'
