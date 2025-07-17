# encoding: utf-8

'''📜 Dicominator tags: custom Django template tags for DICOM data.'''

from django import template
from jpl.labcas.dicominator.tags.models import DicomTag
from wagtail.models import PageQuerySet

register = template.Library()


@register.inclusion_tag('jpl.labcas.dicominator.tags/dicom-tags-table.html')
def dicom_tags_table(query: PageQuerySet[DicomTag]):
    '''Render a table of DICOM tags found for the given page.'''
    return {'dicom_tags': query}
