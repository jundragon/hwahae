from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from hwahae_api.products.models import Product, Category
from hwahae_api.ingredients.models import Ingredient
from hwahae_api.products.serializers import ProductSerializer


class ProductListTest(APITestCase):
    url = reverse("products:list")

    def setUp(self):

        Product.objects.create(name="coffee")
        Product.objects.create(name="potato")

        self.assertEqual(Product.objects.count(), 2)

    def test_상품_목록_조회_응답_시리얼라이저(self):

        response = self.client.get(self.url, format="json")
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"response = {response.status_code}",
        )

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data, f"{response.data}")

    def test_피부타입점수_내림차순_정렬(self):
        # /products?skin_type=oily
        URL_QUERY = "?skin_type=oily"

        Ingredient.objects.create(name="oily1", oily=1)
        Ingredient.objects.create(name="oily2", oily=1)
        Ingredient.objects.create(name="dry1", dry=1)

        product = Product.objects.all()[1]

        for ingredient in Ingredient.objects.all():
            product.ingredients.add(ingredient)

        response = self.client.get(self.url + URL_QUERY, format="json")
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"response = {response.status_code}",
        )

        self.assertEqual(response.data[0]["score_oily"], 2, "피부 타입 정렬 오류")

    def test_피부타입점수_동일할때_가격_오름차순_정렬(self):
        # /products?skin_type=oily
        URL_QUERY = "?skin_type=oily"

        Ingredient.objects.create(name="oily1", oily=1)
        Ingredient.objects.create(name="oily2", oily=1)
        Ingredient.objects.create(name="dry1", dry=1)

        for product in Product.objects.all():
            for ingredient in Ingredient.objects.all():
                product.ingredients.add(ingredient)

        product = Product.objects.all()[0]
        product.price = 1000

        response = self.client.get(self.url + URL_QUERY, format="json")
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"response = {response.status_code}",
        )

        self.assertLess(response.data[0]["price"], 1000, "낮은 가격 정렬 오류")

    def test_필터(self):
        # /products?skin_type=oily&category=skincare
        URL_QUERY = "?skin_type=oily&category=skincare"

        ingredient1 = Ingredient.objects.create(name="oily", oily=1)
        ingredient2 = Ingredient.objects.create(name="dry", dry=1)
        ingredient3 = Ingredient.objects.create(name="sensitive", sensitive=1)

        category = Category.objects.create(name="skincare")

        product = Product.objects.first()
        product.ingredients.add(ingredient1)
        product.ingredients.add(ingredient2)
        product.ingredients.add(ingredient3)
        product.category = category

        response = self.client.get(self.url + URL_QUERY, format="json")
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"response = {response.status_code}",
        )

        # category
        for res in response.data:
            self.assertEqual(res["category"], "skincare", "카테고리 필터 오류")

        # 제외 성분

        # 포함 성분
        pass

    def test_RESPONSE_형식(self):
        pass
