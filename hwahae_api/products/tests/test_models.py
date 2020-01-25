from django.test import TestCase
from hwahae_api.products.models import Product


class ProductModelTest(TestCase):
    # def test_스모크(self):
    #     self.assertEqual(1, 2, "당연히 실패")

    def test_상품모델세이브_AND_마이그레이션테스트(self):
        product = Product()
        product.name = "첫번째"
        product.price = 1000
        product.monthly_sales = 123
        product.save()

        saved_products = Product.objects.all()
        self.assertEqual(saved_products.count(), 1)

        product_saved = saved_products[0]

        self.assertEqual(product_saved.name, "첫번째")
        self.assertEqual(product_saved.price, 1000)
        self.assertEqual(product_saved.monthly_sales, 123)
