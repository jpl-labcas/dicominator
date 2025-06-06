# encoding: utf-8

from django.apps import AppConfig

'''📜 Dicominator DICOM tags: Django apps config.'''


class DicominatorTagsConfig(AppConfig):
    '''The Dicominator tags app.'''
    name = 'jpl.labcas.dicominator.tags'
    label = 'jpllabcasdicominatortags'
    verbose_name = 'Dicominator tags'
