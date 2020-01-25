from django.test import TestCase
from hwahae_api.ingredients.models import Ingredient


class IngredientModelTest(TestCase):
    # def test_스모크(self):
    #     self.assertEqual(1, 2, "당연히 실패")

    def test_성분모델세이브_AND_마이그레이션테스트(self):
        first_ingredient = Ingredient()
        first_ingredient.name = "첫번째"
        first_ingredient.save()

        second_ingredient = Ingredient()
        second_ingredient.name = "두번째"
        second_ingredient.save()

        saved_ingredients = Ingredient.objects.all()
        self.assertEqual(saved_ingredients.count(), 2)

        first_ingredient_saved = saved_ingredients[0]
        second_ingredient_saved = saved_ingredients[1]

        self.assertEqual(first_ingredient_saved.name, "첫번째")
        self.assertEqual(second_ingredient_saved.name, "두번째")
