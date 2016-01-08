import unicodedata

from desafio.core.models import UploadFile
from desafio.core.views import billing_file
from django.test import TestCase
from django.utils.timezone import now


__author__ = 'lucas'


class BillingTest(TestCase):
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

        UploadFile.bulk_insert(self.list_content)

    def test_billing(self):
        value = billing_file(self.import_name)
        self.assertEqual(95, value)

