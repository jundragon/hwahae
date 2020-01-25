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
from hwahae_api.products.models import Product


class SeedDataFunctionalTest(TestCase):

    """ 상품과 성분 json 데이터 입력을 테스트 합니다 """

    @classmethod
    def setUpTestData(cls):
        call_command(
            "seed_ingredients", "hwahae_api/ingredients/fixtures/ingredient-data.json"
        )
        call_command("seed_products", "hwahae_api/products/fixtures/item-data.json")

    def test_성분_데이터_1000개_생성_확인(self):
        count = Ingredient.objects.count()
        self.assertEqual(count, 1000, f"데이터 생성 개수 : {count} ")

    def test_성분_데이터_확인(self):
        first = Ingredient.objects.first()
        self.assertEqual(first.name, "foundation")
        self.assertEqual(first.oily, 0)
        self.assertEqual(first.dry, 0)
        self.assertEqual(first.sensitive, 1)

    def test_상품_데이터_1000개_생성_확인(self):
        count = Product.objects.count()
        self.assertEqual(count, 1000, f"데이터 생성 개수 : {count} ")

    def test_상품_데이터_확인(self):
        first = Product.objects.first()

        print(first.ingredients)

        self.assertEqual(first.name, "리더스 링클 콜라겐 마스크")
        self.assertEqual(first.image_id, "a18de8cd-c730-4f36-b16f-665cca908c11")
        self.assertEqual(first.price, 520)
        self.assertEqual(first.gender, "female")
        self.assertEqual(str(first.category), "suncare")
        self.assertEqual(first.monthly_sales, 5196)
        self.assertEqual(first.ingredients.count(), 5)
