# encoding: utf-8

'''📜 Dicominator tags: DICOM tag handling.'''

import pydicom
from typing import Generator

def top_level_data_elements(ds: pydicom.Dataset) -> Generator[pydicom.DataElement, None, None]:
    '''Yields only the top-level data elements in the given DICOM dataset wihtout recursing into subsequences.'''
    for elem in ds: yield elem
