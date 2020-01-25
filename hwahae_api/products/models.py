from django.db import models
from hwahae_api.core import models as core_models


class Category(core_models.AbstractItem):

    """ Category Model Definition """

    class Meta:
        verbose_name_plural = "Categories"


class Product(core_models.TimeStampedModel):

    """ Product Model Definition """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_ALL = "all"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_ALL, "All"),
    )

    image_id = models.CharField(max_length=80)
    name = models.CharField(max_length=32)
    price = models.IntegerField(help_text="KRW", default=0)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default=GENDER_ALL,
    )
    category = models.ForeignKey(
        "Category", related_name="products", on_delete=models.SET_NULL, null=True,
    )
    ingredients = models.ManyToManyField(
        "ingredients.Ingredient", related_name="products"
    )
    monthly_sales = models.IntegerField(help_text="이번 달 판매 수량", default=0)

    def __str__(self):
        return self.name

    @staticmethod
    def sum_score(_query, _type):
        ingredients = _query
        if len(ingredients) <= 0:
            return 0
        score = 0
        for ingredient in ingredients:
            if _type == "oily":
                score += ingredient.oily
            elif _type == "dry":
                score += ingredient.dry
            elif _type == "sensitive":
                score += ingredient.sensitive
        return score

    def score_oily(self):
        return self.sum_score(self.ingredients.all(), "oily")

    def score_dry(self):
        return self.sum_score(self.ingredients.all(), "dry")

    def score_sensitive(self):
        return self.sum_score(self.ingredients.all(), "sensitive")

    class Meta:
        ordering = ["pk"]
