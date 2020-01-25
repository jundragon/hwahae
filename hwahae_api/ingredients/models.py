from hwahae_api.core import models as core_models


class Ingredient(core_models.AbstractItem):

    """ Ingredient Model Definition """

    def __str__(self):
        return self.name
