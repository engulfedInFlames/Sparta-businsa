from datetime import date
from django.db import models
from common.models import CommonModel
from django.conf import settings


class Inbound(CommonModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default="",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
    date = models.DateField(
        default=date.today,
    )
