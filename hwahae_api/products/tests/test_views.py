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

        self.response = self.client.get(self.url, format="json")
        self.assertEqual(
            self.response.status_code,
            status.HTTP_200_OK,
            f"response = {self.response.status_code}",
        )

    def test_상품_목록_조회_응답_시리얼라이저(self):

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(self.response.data, serializer.data, f"{self.response.data}")

    def test_RESPONSE_형식(self):
        pass

    def test_피부타입_낮은가격_정렬(self):
        pass

    def test_필터(self):
        # 제외 성분

        # 포함 성분
        pass
