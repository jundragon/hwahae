from django.test import TestCase
from hwahae_api.products.models import Product, Category
from hwahae_api.products.serializers import ProductSerializer, CategorySerializer


class CategorySerializerTest(TestCase):
    def setUp(self):
        self.model = Category()
        self.model.name = "테스트용 카테고리"
        self.serializer = CategorySerializer(instance=self.model)

    def test_data_확인(self):

        self.assertEqual(
            self.serializer.data["name"], "테스트용 카테고리", f"{self.serializer.data}"
        )


class ProductSerializerTest(TestCase):
    def setUp(self):
        category = Category()
        category.name = "테스트용 카테고리"
        self.model = Product.objects.create()  # serializer 에 id가 있으므로 매니저로 생성
        self.model.name = "테스트용 상품"
        self.model.category = category
        self.serializer = ProductSerializer(instance=self.model)

    def test_data_확인(self):

        self.assertEqual(
            self.serializer.data["name"], "테스트용 상품", f"{self.serializer.data}"
        )
        category = self.serializer.data["category"]
        self.assertEqual(
            category["name"], "테스트용 카테고리", f"{self.serializer.data}",
        )
