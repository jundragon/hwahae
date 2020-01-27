from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from hwahae_api.products.models import Product, Category
from hwahae_api.ingredients.models import Ingredient
from hwahae_api.products.serializers import ProductSerializer


class ProductListTest(APITestCase):
    url = reverse("products:list")

    def setUp(self):

        self.product1 = Product.objects.create(name="coffee")
        self.product2 = Product.objects.create(name="potato")

        # 성분 추가
        self.oily1 = Ingredient.objects.create(name="oily1", oily=1)
        self.oily2 = Ingredient.objects.create(name="oily2", oily=1)
        self.dry1 = Ingredient.objects.create(name="dry", dry=1)
        self.sensitive1 = Ingredient.objects.create(name="sensitive1", sensitive=1)

        for ingredient in Ingredient.objects.all():
            self.product2.ingredients.add(
                ingredient
            )  # 두번째 객체에 높은 스코어를 부여하여 정렬 후 결과를 확인하기

        self.product1.ingredients.add(self.sensitive1)

        self.assertEqual(Product.objects.count(), 2, "생성 확인")

    def test_상품_목록_조회_응답(self):

        URL_QUERY = "?skin_type=oily"
        response = self.client.get(self.url + URL_QUERY, format="json")

        self.assertEqual(
            response.status_code, status.HTTP_200_OK, "응답 상태 확인",
        )

    def test_피부타입점수_내림차순_정렬(self):
        # /products?skin_type=oily
        URL_QUERY = "?skin_type=oily"

        response = self.client.get(self.url + URL_QUERY, format="json")

        self.assertEqual(response.data[0]["name"], self.product2.name, "피부 타입 정렬 오류")

    def test_피부타입점수_동일할때_가격_오름차순_정렬(self):
        # /products?skin_type=oily
        URL_QUERY = "?skin_type=oily"

        self.product2.price = 1000

        response = self.client.get(self.url + URL_QUERY, format="json")

        self.assertLess(response.data[0]["price"], 1000, "낮은 가격 정렬 오류")

    def test_카테고리_필터(self):
        # /products?skin_type=oily&category=skincare
        URL_QUERY = "?skin_type=oily&category=skincare"

        self.product2.category = Category.objects.create(name="skincare")

        response = self.client.get(self.url + URL_QUERY, format="json")

        for res in response.data:  # 응답 결과 전체를 확인하기 위해 반복문 사용
            self.assertEqual(res["category"], "skincare", "카테고리 필터 오류")

    def test_제외성분_필터(self):
        # /products?skin_type=oily&exclude_ingredient=oily
        EXCLUDE_ITEM1 = "oily1"
        EXCLUDE_ITEM2 = "dry1"
        URL_QUERY = f"?skin_type=oily&exclude_ingredient={EXCLUDE_ITEM1}"

        # 제외 성분
        response = self.client.get(self.url + URL_QUERY, format="json")

        for res in response.data:
            self.assertNotIn(EXCLUDE_ITEM1, res["ingredients"], "제외성분 필터 오류")

        # 추가 제외 성분
        URL_QUERY = URL_QUERY + "," + EXCLUDE_ITEM2

        banana = Product.objects.create(name="banana")
        banana.ingredients.add(self.dry1)

        response = self.client.get(self.url + URL_QUERY, format="json")

        for res in response.data:
            self.assertNotIn(EXCLUDE_ITEM1, res["ingredients"], "제외성분 필터 오류")
            self.assertNotIn(EXCLUDE_ITEM2, res["ingredients"], "추가 제외성분 필터 오류")

    def test_포함성분_필터(self):
        # /products?skin_type=oily&include_ingredient=oily
        URL_QUERY = "?skin_type=oily&include_ingredient=oily"
        INCLUDE_ITEM1 = "oily1"
        INCLUDE_ITEM2 = "dry1"
        URL_QUERY = f"?skin_type=oily&include_ingredient={INCLUDE_ITEM1}"

        # 포함 성분
        response = self.client.get(self.url + URL_QUERY, format="json")

        for res in response.data:
            self.assertIn(INCLUDE_ITEM1, res["ingredients"], "포함성분 필터 오류")

        # 추가 포함 성분
        URL_QUERY = URL_QUERY + "," + INCLUDE_ITEM2

        banana = Product.objects.create(name="banana")
        banana.ingredients.add(self.dry1)

        response = self.client.get(self.url + URL_QUERY, format="json")

        for res in response.data:
            self.assertIn(INCLUDE_ITEM1, res["ingredients"], "포함성분 필터 오류")
            self.assertIn(INCLUDE_ITEM2, res["ingredients"], "추가 포함성분 필터 오류")
