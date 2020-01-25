"""
# 피부 타입마다 성분 기반으로 화장품을 추천해주는 서비스
# RESTful API 기능 테스트

# fixture data DB(model) 입력 확인

1. item-data.json
2. ingredient-data.json

"""

from django.core.management import call_command
from django.test import TestCase
from hwahae_api.ingredients.models import Ingredient


class IngredientSeedDataFunctionalTest(TestCase):
    def setUp(self):
        call_command(
            "seed_ingredients", "hwahae_api/ingredients/fixtures/ingredient-data.json"
        )

    # def test_스모크(self):
    #     self.assertEqual(1, 2, "당연히 실패")
    #     pass

    def test_데이터_1000개_생성_확인(self):
        count = Ingredient.objects.count()
        self.assertEqual(count, 1000, f"데이터 생성 개수 : {count} ")

    def test_데이터_확인(self):
        first = Ingredient.objects.first()
        self.assertEqual(first.name, "foundation")
        self.assertEqual(first.oily, 0)
        self.assertEqual(first.dry, 0)
        self.assertEqual(first.sensitive, 1)
