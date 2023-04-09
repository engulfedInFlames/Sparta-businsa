from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    def __str__(self) -> str:
        return self.username

    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices
    )
