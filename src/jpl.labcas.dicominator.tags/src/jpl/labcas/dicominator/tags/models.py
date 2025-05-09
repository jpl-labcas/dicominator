# encoding: utf-8

'''📜 Dicominator: DICOM tag and other related models.'''

from django.db import models


class Patient(models.Model):
    patient_id = models.CharField(
        max_length=32, null=False, blank=False, default='0',
        help_text='DICOM patient identifier'
    )
    sex = models.CharField(
        max_length=1, choices=('M', 'F', 'O'), default='O', null=False, blank=False,
        help_text='Gender and/or sex'
    )
    birth_date = models.DateField(null=True, help_text='Patient date of birth, de-identified before saving')
    other_attributes = models.JSONField(null=True, help_text='Optional demographic metadata')


class Study(models.Model):
    instance_uid = models.CharField(primary_key=True, null=False, blank=False, default='0', help_text='Unique study ID')
    patient_id = models.ForeignKey(Patient, on_delete=models.SET_NULL)
    study_date = models.DateField(null=True, help_text='When this study started or concluded?')
    description = models.TextField(help_text='Summary description of this study')
    accession_number = models.CharField(null=False, blank=True, help_text='TBD')
    institution_name = models.CharField(null=False, blank=True, help_text='Name of the site conducting the study')


class Series(models.Model):
    instance_uid = models.CharField(
        primary_key=True, null=False, blank=False, default='0', help_text='Unique series ID'
    )
    study_instance = models.ForeignKey(Study, on_delete=models.SET_NULL)
    series_number = models.IntField(default=0, help_text='Series number within the study')
    description = models.TextField(help_text='Summary description of this series')
    modality = models.CharField(null=False, blank=True, help_text='CT, MR, PET, etc.')
    body_part_examined = models.CharField(null=False, blank=True, help_text='Body system or organ')
    series_date = models.DateField(null=True, help_text='When this series started or concluded?')
    manufacturer = models.CharField(null=False, blank=True, help_text='Who made the instrument')
    software_versions = models.CharField(null=False, blank=True, help_text='Version (semantic or otherwise)')


class Image(models.Model):
    series_instance = models.ForeignKey(Series, on_delete=models.SET_NULL)
    image_number = models.IntField(null=False, default=0, help_text='Slice/instance number')
    slice_thickness = models.FloatField(null=False, default=0.0)
