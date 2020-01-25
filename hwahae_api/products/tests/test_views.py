from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from hwahae_api.products.models import Product
from hwahae_api.products.serializers import ProductSerializer


class ProductListTest(APITestCase):
    url = reverse("products:list")

    def setUp(self):
        Product.objects.create(name="coffee")
        Product.objects.create(name="potato")

        self.assertEqual(Product.objects.count(), 2)

    def test_상품_목록_APIVIEW_응답_시리얼라이저(self):
        response = self.client.get(self.url, format="json")
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"response = {response.status_code}",
        )
        self.assertEqual(response.data, serializer.data, f"{response.data}")
