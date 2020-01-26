from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from hwahae_api.products.models import Product
from hwahae_api.ingredients.models import Ingredient
from hwahae_api.products.serializers import ProductSerializer


class ProductListTest(APITestCase):
    url = reverse("products:list")

    def setUp(self):
        Ingredient.objects.create(name="executrix")
        Ingredient.objects.create(name="provision")
        Ingredient.objects.create(name="multimedia")

        coffee = Product.objects.create(name="coffee")

        for ingredient in Ingredient.objects.all():
            coffee.ingredients.add(ingredient)

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

    def test_상품_성분_리스트_문자열_출력(self):
        """
            ["executrix", "provision", "multimedia"] -> "executrix,provision,multimedia"
            콤마로 구분된 하나의 문자열로 반환
        """
        TEST_INGREDIENT = "executrix,provision,multimedia"

        product = Product.objects.get(name="coffee")
        serializer = ProductSerializer(product)

        self.assertEqual(
            serializer.data["ingredients"],
            TEST_INGREDIENT,
            f"성분 리스트 출력 형식이 다릅니다 : {serializer.data['ingredients']}",
        )

    def test_이미지_URL(self):
        pass

    def test_RESPONSE_형식(self):
        pass

    def test_피부타입_낮은가격_정렬(self):
        pass

    def test_필터(self):
        # 제외 성분

        # 포함 성분
        pass
