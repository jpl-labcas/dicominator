# encoding: utf-8

'''📜 Dicominator: DICOM tag and other related models.'''

from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel


class Patient(Page):
    patient_id = models.CharField(max_length=64, unique=True)
    patient_sex = models.CharField(max_length=10, null=True, blank=True)
    patient_birth_date = models.DateField(null=True, blank=True)
    other_attributes = models.JSONField(null=True, blank=True)

    template = 'jpl.labcas.dicominator.tags/patient-page.html'

    # Only PatientIndex can be a parent of Patient
    parent_page_types = ['jpllabcasdicominatortags.PatientIndex']
    
    # Patient can have Study pages as children
    subpage_types = ['jpllabcasdicominatortags.Study']

    content_panels = Page.content_panels + [
        FieldPanel('patient_id'),
        FieldPanel('patient_sex'),
        FieldPanel('patient_birth_date'),
        FieldPanel('other_attributes'),
    ]

    def __str__(self):
        return self.patient_id


class Study(Page):
    study_instance_uid = models.CharField(max_length=128, unique=True)
    study_date = models.DateField(null=True, blank=True)
    study_description = models.TextField(null=True, blank=True)
    accession_number = models.CharField(max_length=64, null=True, blank=True)
    institution_name = models.CharField(max_length=128, null=True, blank=True)

    template = 'jpl.labcas.dicominator.tags/study-page.html'

    # Only Patient can be a parent of Study
    parent_page_types = ['jpllabcasdicominatortags.Patient']
    
    # Study can have Series pages as children
    subpage_types = ['jpllabcasdicominatortags.Series']

    content_panels = Page.content_panels + [
        FieldPanel('study_instance_uid'),
        FieldPanel('study_date'),
        FieldPanel('study_description'),
        FieldPanel('accession_number'),
        FieldPanel('institution_name'),
    ]

    def __str__(self):
        return self.study_instance_uid


class Series(Page):
    series_instance_uid = models.CharField(max_length=128, unique=True)
    series_number = models.IntegerField(null=True, blank=True)
    series_description = models.TextField(null=True, blank=True)
    modality = models.CharField(max_length=16, null=True, blank=True)
    body_part_examined = models.CharField(max_length=64, null=True, blank=True)
    series_date = models.DateField(null=True, blank=True)
    manufacturer = models.CharField(max_length=128, null=True, blank=True)
    software_versions = models.CharField(max_length=128, null=True, blank=True)

    template = 'jpl.labcas.dicominator.tags/series-page.html'

    # Only Study can be a parent of Series
    parent_page_types = ['jpllabcasdicominatortags.Study']
    
    # Series can have Image pages as children
    subpage_types = ['jpllabcasdicominatortags.Image']

    content_panels = Page.content_panels + [
        FieldPanel('series_instance_uid'),
        FieldPanel('series_number'),
        FieldPanel('series_description'),
        FieldPanel('modality'),
        FieldPanel('body_part_examined'),
        FieldPanel('series_date'),
        FieldPanel('manufacturer'),
        FieldPanel('software_versions'),
    ]

    def __str__(self):
        return self.series_instance_uid


class Image(Page):
    sop_instance_uid = models.CharField(max_length=128, unique=True)
    image_number = models.IntegerField(null=True, blank=True)
    slice_thickness = models.FloatField(null=True, blank=True)
    pixel_spacing = models.CharField(max_length=64, null=True, blank=True)
    image_orientation = models.CharField(max_length=128, null=True, blank=True)

    template = 'jpl.labcas.dicominator.tags/image-page.html'

    # Only Series can be a parent of Image
    parent_page_types = ['jpllabcasdicominatortags.Series']
    
    # Image pages are leaf nodes - they can't have children
    subpage_types = []

    content_panels = Page.content_panels + [    
        FieldPanel('sop_instance_uid'),
        FieldPanel('image_number'),
        FieldPanel('slice_thickness'),
        FieldPanel('pixel_spacing'),
        FieldPanel('image_orientation'),
    ]

    def __str__(self):
        return self.sop_instance_uid


class DicomTag(Page):
    LEVEL_CHOICES = [
        ('study', 'Study'),
        ('series', 'Series'),
        ('instance', 'Instance'),
    ]

    uid = models.CharField(max_length=128)  # Referencing Study, Series, or SOPInstanceUID
    level = models.CharField(max_length=16, choices=LEVEL_CHOICES)
    tag = models.CharField(max_length=16)  # e.g. (0010,0010)
    tag_name = models.CharField(max_length=128)
    vr = models.CharField(max_length=4, null=True, blank=True)  # Value Representation
    value = models.TextField(null=True, blank=True)

    template = 'jpl.labcas.dicominator.tags/dicom-tag-page.html'

    # DicomTag pages can be children of Study, Series, or Image pages
    parent_page_types = [
        'jpllabcasdicominatortags.Study',
        'jpllabcasdicominatortags.Series',
        'jpllabcasdicominatortags.Image'
    ]
    
    # DicomTag pages are leaf nodes
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel('uid'),
        FieldPanel('level'),
        FieldPanel('tag'),
        FieldPanel('tag_name'),
        FieldPanel('vr'),
        FieldPanel('value'),
    ]

    def __str__(self):
        return f"{self.level.upper()}:{self.tag_name} = {self.value}"


class CancerLabel(Page):
    uid = models.CharField(max_length=128)  # Referencing Study or Series UID
    cancer_type = models.CharField(max_length=64)
    diagnosis_date = models.DateField(null=True, blank=True)
    stage = models.CharField(max_length=32, null=True, blank=True)

    template = 'jpl.labcas.dicominator.tags/cancer-label-page.html'

    # CancerLabel pages can be children of Study or Series pages
    parent_page_types = [
        'jpllabcasdicominatortags.Study',
        'jpllabcasdicominatortags.Series'
    ]
    
    # CancerLabel pages are leaf nodes
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel('uid'),
        FieldPanel('cancer_type'),
        FieldPanel('diagnosis_date'),
        FieldPanel('stage'),
    ]

    def __str__(self):
        return f"{self.cancer_type} ({self.stage})"
    

class PatientIndex(Page):
    '''Index page for Patient pages.'''
    
    template = 'jpl.labcas.dicominator.tags/patient-index-page.html'
    
    # PatientIndex can be a child of HomePage or FlexPage
    parent_page_types = [
        'jpllabcasdicominatorcontent.HomePage',
        'jpllabcasdicominatorcontent.FlexPage'
    ]
    
    # PatientIndex can have Patient pages as children
    subpage_types = ['jpllabcasdicominatortags.Patient']
