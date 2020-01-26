from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from hwahae_api.products.models import Product
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

    def test_피부타입_점수_내림차순_정렬(self):
        # /products?skin_type=oily
        ORDERING_QUERY = "?skin_type=oily"

        Ingredient.objects.create(name="oily1", oily=1)
        Ingredient.objects.create(name="oily2", oily=1)
        Ingredient.objects.create(name="dry1", dry=1)

        product = Product.objects.all()[1]

        for ingredient in Ingredient.objects.all():
            product.ingredients.add(ingredient)

        response = self.client.get(self.url + ORDERING_QUERY, format="json")
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"response = {response.status_code}",
        )

        self.assertEqual(response.data[0]["score_oily"], 2, "피부 타입 정렬 오류")

    def test_피부타입_동일할때_가격_오름차순_정렬(self):
        # /products?skin_type=oily

        pass

    def test_필터(self):
        # 제외 성분

        # 포함 성분
        pass

    def test_RESPONSE_형식(self):
        pass

