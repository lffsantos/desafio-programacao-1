from django.db import models


class UploadFile(models.Model):
    import_name = models.CharField(max_length=100)
    purchaser_name = models.CharField(max_length=100)
    item_description = models.CharField(max_length=255)
    item_price = models.FloatField()
    purchase_count = models.IntegerField()
    merchant_address = models.CharField(max_length=255)
    merchant_name = models.CharField(max_length=255)

    def unpack_line(self, line, import_name):
        self.import_name = import_name

        self.purchaser_name, self.item_description, \
        self.item_price, self.purchase_count, \
        self.merchant_address, self.merchant_name = line
        return self

    @staticmethod
    def bulk_insert(list_content_file, batch_size=999):
        UploadFile.objects.bulk_create(list_content_file, batch_size)
