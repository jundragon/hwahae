from django.test import TestCase
from hwahae_api.ingredients.models import Ingredient
from hwahae_api.ingredients.serializers import IngredientSerializer


class IngredientSerializerTest(TestCase):
    def setUp(self):
        self.model = Ingredient()
        self.model.name = "테스트용 성분"
        self.serializer = IngredientSerializer(instance=self.model)

    def test_data_확인(self):

        self.assertEqual(
            self.serializer.data["name"], "테스트용 성분", f"{self.serializer.data}"
        )
        pass
