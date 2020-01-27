from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from hwahae_api.products.models import Product, Category
from hwahae_api.ingredients.models import Ingredient
from hwahae_api.products.serializers import ProductSerializer, ProductDetailSerializer


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

        self.assertEqual(response.data[0]["name"], product.name, "피부 타입 정렬 오류")

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

    def test_카테고리_필터(self):
        # /products?skin_type=oily&category=skincare
        URL_QUERY = "?skin_type=oily&category=skincare"

        product = Product.objects.first()
        category = Category.objects.create(name="skincare")
        product.category = category

        # category filter test
        response = self.client.get(self.url + URL_QUERY, format="json")
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"response = {response.status_code}",
        )

        for res in response.data:
            self.assertEqual(res["category"], "skincare", "카테고리 필터 오류")

    def test_제외성분_필터(self):
        # /products?skin_type=oily&exclude_ingredient=oily
        URL_QUERY = "?skin_type=oily&exclude_ingredient=oily"

        ingredient1 = Ingredient.objects.create(name="oily", oily=1)
        ingredient2 = Ingredient.objects.create(name="dry", dry=1)
        ingredient3 = Ingredient.objects.create(name="sensitive", sensitive=1)

        product = Product.objects.first()
        product.ingredients.add(ingredient1)
        product.ingredients.add(ingredient2)
        product.ingredients.add(ingredient3)

        # 제외 성분
        response = self.client.get(self.url + URL_QUERY, format="json")
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"response = {response.status_code}",
        )

        for res in response.data:
            self.assertNotIn("oily", res["ingredients"], "제외성분 필터 오류")

        # 제외 성분 콤마로 구분
        URL_QUERY = URL_QUERY + ",dry"

        banana = Product.objects.create(name="banana")
        banana.ingredients.add(ingredient2)

        response = self.client.get(self.url + URL_QUERY, format="json")

        for res in response.data:
            self.assertNotIn("oily", res["ingredients"], "다수개의 제외성분 필터 오류")

    def test_포함성분_필터(self):
        # /products?skin_type=oily&include_ingredient=oily
        URL_QUERY = "?skin_type=oily&include_ingredient=oily"

        ingredient1 = Ingredient.objects.create(name="oily", oily=1)
        ingredient2 = Ingredient.objects.create(name="dry", dry=1)
        ingredient3 = Ingredient.objects.create(name="sensitive", sensitive=1)

        product = Product.objects.first()
        product.ingredients.add(ingredient1)
        product.ingredients.add(ingredient2)
        product.ingredients.add(ingredient3)

        # 포함 성분
        response = self.client.get(self.url + URL_QUERY, format="json")
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"response = {response.status_code}",
        )

        for res in response.data:
            self.assertIn("oily", res["ingredients"], "포함성분 필터 오류")

        # 포함 성분 콤마로 구분
        URL_QUERY = URL_QUERY + ",dry"

        banana = Product.objects.create(name="banana")
        banana.ingredients.add(ingredient2)

        response = self.client.get(self.url + URL_QUERY, format="json")

        for res in response.data:
            self.assertIn("oily", res["ingredients"], "다수개의 포함성분 필터 오류")
            self.assertIn("dry", res["ingredients"], "다수개의 포함성분 필터 오류")


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

        Ingredient.objects.create(name="oily", oily=1)
        Ingredient.objects.create(name="dry", dry=1)
        Ingredient.objects.create(name="sensitive", sensitive=1)

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

        self.assertEqual(Product.objects.count(), 5)

    def test_상품_정보_조회_응답_시리얼라이저(self):

        response = self.client.get(self.url(pk=1), format="json")
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"response = {response.status_code}",
        )

        products = Product.objects.all()
        serializer = ProductDetailSerializer(products, many=True)
        self.assertEqual(response.data[0], serializer.data[0], "예상한 응답과 다릅니다")

    def test_상품_상세_정보_조회(self):

        response = self.client.get(self.url(pk=1), format="json")
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.status_code,
        )

        TEST_THUMBNAIL = "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/a18de8cd-c730-4f36-b16f-665cca908c11.jpg"

        test_data = {
            "id": 1,
            "imgUrl": TEST_THUMBNAIL,
            "name": self.sample_data["name"],
            "price": self.sample_data["price"],
            "gender": self.sample_data["gender"],
            "category": "skincare",
            "ingredients": "oily,dry,sensitive",
            "monthlySales": self.sample_data["monthly_sales"],
        }

        self.assertEqual(response.data[0], test_data, "예상한 응답과 다릅니다")

    def test_추천상품정보_조회(self):
        # /product/1?skin_type=oily
        URL_QUERY = "?skin_type=oily"

        response = self.client.get(self.url(pk=1) + URL_QUERY, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, response.status_code,
        )

        TEST_THUMBNAIL = "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/a18de8cd-c730-4f36-b16f-665cca908c11.jpg"

        test_data1 = {"id": 2, "imgUrl": TEST_THUMBNAIL, "name": "potato", "price": 50}
        test_data2 = {"id": 4, "imgUrl": TEST_THUMBNAIL, "name": "melon", "price": 100}
        test_data3 = {"id": 3, "imgUrl": TEST_THUMBNAIL, "name": "banana", "price": 150}

        self.assertEqual(dict(response.data[1]), test_data1, "예상한 응답과 다릅니다")
        self.assertEqual(dict(response.data[2]), test_data2, "예상한 응답과 다릅니다")
        self.assertEqual(dict(response.data[3]), test_data3, "예상한 응답과 다릅니다")
