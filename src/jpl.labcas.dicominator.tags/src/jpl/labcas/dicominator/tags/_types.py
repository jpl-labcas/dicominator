# encoding: utf-8

'''📜 Dicominator: types and other interesting things.'''

from enum import Enum


class TagClassification(Enum):
    '''Classification of DICOM tags.'''
    STUDY = 1
    SERIES = 2
    IMAGE = 3


CLASSIFICATION_TO_ENUM = {
    'Study': TagClassification.STUDY,
    'Series': TagClassification.SERIES,
    'Instance': TagClassification.IMAGE,
}
