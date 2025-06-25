# encoding: utf-8

'''📜 Dicominator: load data from DICOM files.'''

from typing import Generator
from django.conf import settings
from django.core.management.base import BaseCommand
from jpl.labcas.dicominator.content.models import HomePage
from jpl.labcas.dicominator.tags.models import PatientIndex, Patient, Study, Series, Image, DicomTag, CancerLabel
import argparse, os, pydicom


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

    def _add_study(self, patient: Patient, dicom_obj: pydicom.FileDataset):
        '''Adds a study to the patient.'''
        study = Study.objects.filter(study_instance_uid=dicom_obj.StudyInstanceUID).first()
        if study is None:
            study = Study(study_instance_uid=dicom_obj.StudyInstanceUID, title=dicom_obj.StudyInstanceUID)
            patient.add_child(instance=study)
            study.save()
        else:
            # Update the study; TBD
            pass

    def _load_dicom_files(self, folder: str, slug: str):
        '''Loads DICOM files from the given folder into the Dicominator.'''
        self.stdout.write(f'🚶 Loading DICOM files from {folder} into {slug}')
        patient_index = PatientIndex.objects.filter(slug=slug).first()
        if patient_index is None:
            self.stderr.write(f'💥 PatientIndex with slug «{slug}» not found; aborting')
            return
        for fn, dicom_obj in self._generate_dicom_files(folder):
            try:
                patient = Patient.objects.filter(patient_id=dicom_obj.PatientID).first()
                if patient is None:
                    patient = Patient(
                        patient_id=dicom_obj.PatientID, title=dicom_obj.PatientID, slug=dicom_obj.PatientID
                    )
                    patient_index.add_child(instance=patient)
                    patient.save()
                else:
                    # TBD: update patient
                    pass
                self._add_study(patient, dicom_obj)
            except AttributeError as ex:
                self.stderr.write(f'🤔 File {fn} was missing a required field: {ex}')
                continue

    def handle(self, *args, **options):
        self.stdout.write('Loading DICOM files into the Dicominator')

        try:
            settings.WAGTAILREDIRECTS_AUTO_CREATE = False
            settings.WAGTAILSEARCH_BACKENDS['default']['AUTO_UPDATE'] = False

            self._load_dicom_files(options['folder'], options['slug'])

        finally:
            settings.WAGTAILREDIRECTS_AUTO_CREATE = True
            settings.WAGTAILSEARCH_BACKENDS['default']['AUTO_UPDATE'] = True
