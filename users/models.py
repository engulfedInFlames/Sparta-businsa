from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    class GenderKindChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    gender = models.CharField(
        max_length=10,
        choices=GenderKindChoices.choices
    )
