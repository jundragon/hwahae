from django.db import models
from hwahae_api.core import models as core_models


class Category(core_models.AbstractItem):

    """ Category Model Definition """

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(core_models.TimeStampedModel):

    """ Product Model Definition """

    def __str__(self):
        return self.name
