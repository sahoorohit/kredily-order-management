import time

from django.db import models

from utils.models import CustomBaseModel


def generate_product_id() -> str:
    return f'PROD{int(time.time())}'


class Product(CustomBaseModel):

    product_id = models.CharField(max_length=256, blank=False, null=False, default=generate_product_id)
    name = models.CharField(max_length=256, blank=False, null=False)
    price = models.IntegerField(default=0)
    available_quantity = models.IntegerField(default=0)

    def __str__(self):
        return "{}".format(self.name)
