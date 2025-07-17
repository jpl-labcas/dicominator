# encoding: utf-8

'''📜 Dicominator: scan DICOM tag frequencies over massive sets of DICOM files in a folder.'''

from django.core.management.base import BaseCommand
from collections import Counter
from multiprocessing import Queue, Process, cpu_count
from pydicom.errors import InvalidDicomError
from pydicom.datadict import keyword_for_tag, dictionary_description
from jpl.labcas.dicominator.tags.templatetags.tag_handling import top_level_data_elements
import argparse, os, pydicom, sys





def file_consumer(queue: Queue):
    import django
    django.setup()
    from django.db import connections, close_old_connections, transaction, IntegrityError
    from django.db.models import F
    from jpl.labcas.dicominator.tags.models import TagFrequency, SurveyedFile

    close_old_connections()
    for conn in connections.all():
        conn.close()

    local_counter = Counter()
    while True:
        path = queue.get()
        if path is None: break

        # No race here because each worker gets its own set of files to process
        if SurveyedFile.objects.filter(file_path=path).exists(): continue

        try:
            ds = pydicom.dcmread(path, stop_before_pixels=True)
        except InvalidDicomError as ex:
            print(f'🤷 Cannot load {path} as a DICOM file, skipping ({ex})', file=sys.stderr)
            continue
        for elem in top_level_data_elements(ds):
            # Skip sequences; we want only top-level element scalars and private tags
            if elem.VR == 'SQ' or elem.tag.is_private or elem.tag.is_private_creator: continue
            local_counter[elem.tag] += 1

        # No race here because each worker gets its own set of files to process
        SurveyedFile.objects.get_or_create(file_path=path)

    with transaction.atomic():
        for tag, count in local_counter.items():
            try:
                keyword, name = keyword_for_tag(tag) or '«unknown»', dictionary_description(tag) or '«unknown»'
            except KeyError:
                print(f'🤷 Cannot find keyword or description for {tag}', file=sys.stderr)
                continue

            rows_updated = TagFrequency.objects.filter(tag_group=tag.group, tag_element=tag.element).update(
                frequency=F('frequency') + count
            )
            if rows_updated == 0:
                try:
                    with transaction.atomic():
                        TagFrequency.objects.create(
                            tag_group=tag.group, tag_element=tag.element, keyword=keyword, name=name,
                            frequency=count
                        )
                except IntegrityError:
                    # Another process has already created this tag frequency, so update again
                    TagFrequency.objects.filter(tag_group=tag.group, tag_element=tag.element).update(
                        frequency=F('frequency') + count
                    )


class Command(BaseCommand):
    help = 'Scans DICOM tag frequencies over sets of DICOM files in a folder.'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('folder', help='Folder containing DICOM files to load')

    def handle(self, *args, **options):
        self.stdout.write('Loading DICOM files into the Dicominator')
        folder = options['folder']
        if not os.path.isdir(folder):
            self.stderr.write(f'💥 Folder {folder} does not exist')
            return
        num_workers = cpu_count()
        file_queue = Queue(maxsize=1000)
        workers = []
        for _ in range(num_workers):
            p = Process(target=file_consumer, args=(file_queue,))
            p.start()
            workers.append(p)
        for root, _, files in os.walk(folder):
            for file in files:
                file_queue.put(os.path.join(root, file))
        for _ in range(num_workers):
            file_queue.put(None)
        for p in workers:
            p.join()
        self.stdout.write('🎉 Done')
