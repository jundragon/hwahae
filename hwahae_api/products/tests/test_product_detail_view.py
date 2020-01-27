from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from hwahae_api.products.models import Product, Category
from hwahae_api.ingredients.models import Ingredient
from hwahae_api.products.serializers import ProductDetailSerializer


class ProductDetailTest(APITestCase):
    def url(self, pk):
        return reverse("products:detail", kwargs={"pk": pk})

    def setUp(self):

        SAMPLE_IMAGE_ID = "a18de8cd-c730-4f36-b16f-665cca908c11"

        category = Category.objects.create(name="skincare")
        self.sample_data = {
            "name": "coffee",
            "price": 1000,
            "gender": "all",
            "monthly_sales": 1234,
            "image_id": SAMPLE_IMAGE_ID,
            "category": category,
        }

        self.oily = Ingredient.objects.create(name="oily", oily=1)
        self.dry = Ingredient.objects.create(name="dry", dry=1)
        self.sensitive = Ingredient.objects.create(name="sensitive", sensitive=1)

        self.sample_product = Product.objects.create(**self.sample_data)
        for ingredient in Ingredient.objects.all():
            self.sample_product.ingredients.add(ingredient)

        Product.objects.create(
            name="potato", price=50, category=category, image_id=SAMPLE_IMAGE_ID
        )
        Product.objects.create(
            name="banana", price=150, category=category, image_id=SAMPLE_IMAGE_ID
        )
        Product.objects.create(
            name="melon", price=100, category=category, image_id=SAMPLE_IMAGE_ID
        )
        Product.objects.create(
            name="chicken", price=200, category=category, image_id=SAMPLE_IMAGE_ID
        )

        self.assertEqual(Product.objects.count(), 5, "생성 확인")

    def test_상품_정보_조회_응답_시리얼라이저(self):

        products = Product.objects.all()
        serializer = ProductDetailSerializer(products, many=True)

        response = self.client.get(self.url(products[0].id), format="json")
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, "응답 상태 확인",
        )

        self.assertEqual(
            response.data[0], serializer.data[0], "시리얼라이저 결과와 API 응답 결과 불일치"
        )

    def test_상품_상세_정보_조회(self):

        product = Product.objects.first()
        response = self.client.get(self.url(product.id), format="json")

        self.assertEqual(response.data[0]["id"], product.id, "상세 정보 조회 오류")

    def test_추천상품정보_조회(self):
        # /product/1?skin_type=oily
        URL_QUERY = "?skin_type=oily"

        product = Product.objects.first()
        response = self.client.get(self.url(product.id) + URL_QUERY, format="json")

        self.assertEqual(response.data[1]["name"], "potato", "예상한 응답과 다릅니다")
        self.assertEqual(response.data[2]["name"], "melon", "예상한 응답과 다릅니다")
        self.assertEqual(response.data[3]["name"], "banana", "예상한 응답과 다릅니다")
