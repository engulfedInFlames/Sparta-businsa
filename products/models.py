from django.db import models
from django.conf import settings
from common.models import CommonModel


class Product(CommonModel):
    # pylint: disable=E0307
    def __str__(self) -> str:
        return self.code

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    code = models.CharField(
        max_length=12,
    )
    name = models.CharField(
        max_length=240,
    )
    price = models.PositiveIntegerField()
    stock = models.PositiveBigIntegerField(
        default=0,
    )
