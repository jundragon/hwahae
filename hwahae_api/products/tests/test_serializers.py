from django.test import TestCase
from hwahae_api.products.models import Product, Category
from hwahae_api.ingredients.models import Ingredient
from hwahae_api.products.serializers import (
    ProductSerializer,
    ProductDetailSerializer,
    ProductRecommendSerializer,
)


TEST_THUMBNAIL = "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/a18de8cd-c730-4f36-b16f-665cca908c11.jpg"


class ProductSerializerTest(TestCase):
    def setUp(self):

        Product.objects.create(name="coffee")
        Product.objects.create(name="potato")

        self.assertEqual(Product.objects.count(), 2, "생성 확인")

    def test_ProductSerializer(self):

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        self.assertEqual(serializer.data[0]["name"], "coffee", "ProductSerializer 오류")

    def test_ProductDetailSerializer(self):

        products = Product.objects.all()
        serializer = ProductDetailSerializer(products, many=True)

        self.assertEqual(
            serializer.data[0]["name"], "coffee", "ProductDetailSerializer 오류"
        )

    def test_ProductRecommendSerializer(self):

        products = Product.objects.all()
        serializer = ProductRecommendSerializer(products, many=True)

        self.assertEqual(
            serializer.data[0]["name"], "coffee", "ProductRecommendSerializer 오류"
        )

    def test_상품_성분_리스트_문자열_출력(self):
        """
            ["executrix", "provision", "multimedia"] -> "executrix,provision,multimedia"
            콤마로 구분된 하나의 문자열로 반환
        """
        TEST_INGREDIENT = "executrix,provision,multimedia"

        Ingredient.objects.create(name="executrix")
        Ingredient.objects.create(name="provision")
        Ingredient.objects.create(name="multimedia")

        product = Product.objects.first()
        product.category = Category.objects.create(name="skincare")

        for ingredient in Ingredient.objects.all():
            product.ingredients.add(ingredient)

        serializer = ProductSerializer(product)

        self.assertEqual(
            serializer.data["ingredients"], TEST_INGREDIENT, "성분 리스트의 출력 형식 문자열 콤마",
        )

    def test_이미지_URL(self):

        product = Product.objects.first()
        product.image_id = "a18de8cd-c730-4f36-b16f-665cca908c11"

        serializer = ProductSerializer(product)

        self.assertEqual(
            serializer.data["imgUrl"], TEST_THUMBNAIL, serializer.data["imgUrl"],
        )
