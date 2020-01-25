from django.db import models
from hwahae_api.core import models as core_models


class Ingredient(core_models.AbstractItem):

    """ Ingredient Model Definition """

    oily = models.IntegerField(default=0)
    dry = models.IntegerField(default=0)
    sensitive = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["pk"]
