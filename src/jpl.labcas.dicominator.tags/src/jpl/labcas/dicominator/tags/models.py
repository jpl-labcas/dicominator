# encoding: utf-8

'''📜 Dicominator: DICOM tag and other related models.'''

from django.db import models


class Patient(models.Model):
    patient_id = models.CharField(max_length=64, unique=True)
    patient_sex = models.CharField(max_length=10, null=True, blank=True)
    patient_birth_date = models.DateField(null=True, blank=True)
    other_attributes = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.patient_id


class Study(models.Model):
    study_instance_uid = models.CharField(max_length=128, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='studies')
    study_date = models.DateField(null=True, blank=True)
    study_description = models.TextField(null=True, blank=True)
    accession_number = models.CharField(max_length=64, null=True, blank=True)
    institution_name = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.study_instance_uid


class Series(models.Model):
    series_instance_uid = models.CharField(max_length=128, unique=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='series')
    series_number = models.IntegerField(null=True, blank=True)
    series_description = models.TextField(null=True, blank=True)
    modality = models.CharField(max_length=16, null=True, blank=True)
    body_part_examined = models.CharField(max_length=64, null=True, blank=True)
    series_date = models.DateField(null=True, blank=True)
    manufacturer = models.CharField(max_length=128, null=True, blank=True)
    software_versions = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.series_instance_uid


class Image(models.Model):
    sop_instance_uid = models.CharField(max_length=128, unique=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='images')
    image_number = models.IntegerField(null=True, blank=True)
    slice_thickness = models.FloatField(null=True, blank=True)
    pixel_spacing = models.CharField(max_length=64, null=True, blank=True)
    image_orientation = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.sop_instance_uid


class DicomTag(models.Model):
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

    def __str__(self):
        return f"{self.level.upper()}:{self.tag_name} = {self.value}"


class CancerLabel(models.Model):
    uid = models.CharField(max_length=128)  # Referencing Study or Series UID
    cancer_type = models.CharField(max_length=64)
    diagnosis_date = models.DateField(null=True, blank=True)
    stage = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return f"{self.cancer_type} ({self.stage})"