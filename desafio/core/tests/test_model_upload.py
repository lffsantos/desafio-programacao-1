import unicodedata

from desafio.core.models import UploadFile
from django.test import TestCase
from django.utils.timezone import now


__author__ = 'lucas'


class UploadFileModelTest(TestCase):
    def setUp(self):
        self.list_content = []
        self.import_name = 'example_input.tab' + str(now())[:19]
        with open('example_input.tab') as data:
            header = False
            for d in data:
                if not header:
                    header = True
                else:
                    upload_file = UploadFile()
                    line = unicodedata.normalize('NFKD', d).encode('ASCII', 'ignore').decode('utf-8').lower().split('\t')
                    upload_file.unpack_line(tuple(line), self.import_name)
                    self.list_content.append(upload_file)

    def test_create(self):
        UploadFile.bulk_insert(self.list_content)
        self.assertEqual(4, len(UploadFile.objects.filter(import_name=self.import_name)))