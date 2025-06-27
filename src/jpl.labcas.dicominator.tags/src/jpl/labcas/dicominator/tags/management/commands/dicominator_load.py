# encoding: utf-8

'''📜 Dicominator: load data from DICOM files.'''

from typing import Generator
from django.conf import settings
from django.core.management.base import BaseCommand
from jpl.labcas.dicominator.content.models import HomePage
from jpl.labcas.dicominator.tags.models import PatientIndex, Patient, Study, Series, Image, DicomTag, CancerLabel
import argparse, os, pydicom


def _add_image(series: Series, dicom_obj: pydicom.FileDataset):
    '''Adds an image to the series.'''
    image = Image.objects.filter(sop_instance_uid=dicom_obj.SOPInstanceUID).first()
    if image is None:
        image = Image(sop_instance_uid=dicom_obj.SOPInstanceUID, title=dicom_obj.SOPInstanceUID)
        series.add_child(instance=image)
    image_number = dicom_obj.get(('0020', '0013'))
    if image_number: image.image_number = image_number.value
    slice_thickness = dicom_obj.get(('0018', '0050'))
    if slice_thickness: image.slice_thickness = slice_thickness.value
    pixel_spacing = dicom_obj.get(('0028', '0030'))
    if pixel_spacing:
        image.pixel_spacing = f'{pixel_spacing.value[0]:.2f} × {pixel_spacing.value[1]:.2f}'
    image_orientation = dicom_obj.get(('0020', '0037'))
    if image_orientation:
        image.image_orientation = ', '.join(f'{v:.2f}' for v in image_orientation.value)
    image.save()


def _add_series(study: Study, dicom_obj: pydicom.FileDataset):
    '''Adds a series to the study.'''
    series = Series.objects.filter(series_instance_uid=dicom_obj.SeriesInstanceUID).first()
    if series is None:
        series = Series(series_instance_uid=dicom_obj.SeriesInstanceUID, title=dicom_obj.SeriesInstanceUID)
        study.add_child(instance=series)
    series_number = dicom_obj.get(('0020', '0011'))
    if series_number: series.series_number = series_number.value
    series_description = dicom_obj.get(('0008', '1030'))
    if series_description: series.series_description = series_description.value
    modality = dicom_obj.get(('0008', '0060'))
    if modality: series.modality = modality.value
    body_part_examined = dicom_obj.get(('0008', '0015'))
    if body_part_examined: series.body_part_examined = body_part_examined.value
    try:
        series_date = dicom_obj.get(('0008', '0021'))
        if series_date: series.series_date = series_date.value
    except Exception as ex:
        pass
    manufacturer = dicom_obj.get(('0008', '0070'))
    if manufacturer: series.manufacturer = manufacturer.value
    software_versions = dicom_obj.get(('0018', '1020'))
    if software_versions:
        if isinstance(software_versions.value, pydicom.multival.MultiValue):
            series.software_versions = ', '.join(software_versions.value)
        else:
            series.software_versions = software_versions.value
    _add_image(series, dicom_obj)
    series.save()


def _add_study(patient: Patient, dicom_obj: pydicom.FileDataset):
    '''Adds a study to the patient.'''
    # Use an existing study if found otherwise create a new one
    study = Study.objects.filter(study_instance_uid=dicom_obj.StudyInstanceUID).first()
    if study is None:
        study = Study(study_instance_uid=dicom_obj.StudyInstanceUID, title=dicom_obj.StudyInstanceUID)
        patient.add_child(instance=study)

    # Update the study with information from the DICOM object
    study_date = dicom_obj.get(('0008', '0020'))
    if study_date: study.study_date = study_date.value
    study_description = dicom_obj.get(('0008', '1030'))
    if study_description: study.study_description = study_description.value
    accession_number = dicom_obj.get(('0008', '0050'))
    if accession_number: study.accession_number = accession_number.value
    institution_name = dicom_obj.get(('0008', '0070'))
    if institution_name: study.institution_name = institution_name.value
    study.save()
    _add_series(study, dicom_obj)


def _update_patient(patient: Patient, dicom_obj: pydicom.FileDataset):
    '''Updates a patient with the given DICOM object.'''
    sex = dicom_obj.get(('0010', '0040'))
    if sex: patient.patient_sex = sex.value
    dob = dicom_obj.get(('0010', '0030'))
    try:
        if dob: patient.patient_birth_date = dob.value
    except Exception as ex:
        pass
    patient.save()
    _add_study(patient, dicom_obj)


class Command(BaseCommand):
    help = 'Loads data from DICOM files into the Dicominator'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('folder', help='Folder containing DICOM files to load')
        parser.add_argument(
            'slug', help='Slug of PatientIndex to contain top-level Patient pages; default %(default)s',
            default='patients', nargs='?'
        )

    def _generate_dicom_files(self, folder: str) -> Generator[pydicom.FileDataset, None, None]:
        '''Generates DICOM files from the given folder.'''
        for parent, b, files in os.walk(folder):
            for fn in files:
                try:
                    yield fn, pydicom.dcmread(os.path.join(parent, fn))
                except Exception as ex:
                    self.stderr.write(f'🤷 Cannot load {fn} as a DICOM file, skipping ({ex})')

    def _load_dicom_files(self, folder: str, slug: str):
        '''Loads DICOM files from the given folder into the Dicominator.'''
        self.stdout.write(f'🚶 Loading DICOM files from {folder} into {slug}')
        patient_index = PatientIndex.objects.filter(slug=slug).first()
        if patient_index is None:
            self.stderr.write(f'💥 PatientIndex with slug «{slug}» not found; aborting')
            return
        count = 0
        for fn, dicom_obj in self._generate_dicom_files(folder):
            try:
                patient = Patient.objects.filter(patient_id=dicom_obj.PatientID).first()
                if patient is None:
                    patient = Patient(
                        patient_id=dicom_obj.PatientID, title=dicom_obj.PatientID, slug=dicom_obj.PatientID
                    )
                    patient_index.add_child(instance=patient)
                _update_patient(patient, dicom_obj)
            except AttributeError as ex:
                self.stderr.write(f'🤔 File {fn} was missing a required field: {ex}')
                continue
            count += 1
            if count % 1000 == 0:
                self.stdout.write(f'🚶 Processed {count} DICOM files')

    def handle(self, *args, **options):
        self.stdout.write('Loading DICOM files into the Dicominator')

        try:
            settings.WAGTAILREDIRECTS_AUTO_CREATE = False
            settings.WAGTAILSEARCH_BACKENDS['default']['AUTO_UPDATE'] = False

            self._load_dicom_files(options['folder'], options['slug'])

        finally:
            settings.WAGTAILREDIRECTS_AUTO_CREATE = True
            settings.WAGTAILSEARCH_BACKENDS['default']['AUTO_UPDATE'] = True
