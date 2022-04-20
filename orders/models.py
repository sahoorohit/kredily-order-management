import uuid

from django.db import models

from accounts.models import User
from utils.models import CustomBaseModel


class Order(CustomBaseModel):

    order_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, blank=False, null=False)
    amount = models.IntegerField(default=0)
    customer = models.ForeignKey(User, related_name="orders", on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.order_id)


class SubOrder(CustomBaseModel):
    item_name = models.CharField(max_length=256, blank=False, null=False)
    unit_price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)

    order = models.ForeignKey(Order, related_name="suborders", on_delete=models.PROTECT)
