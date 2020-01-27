import json
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from hwahae_api.products.models import Product, Category
from hwahae_api.ingredients.models import Ingredient


class Command(BaseCommand):

    """ hwahae_api/products/fixtures/item-data.json """

    help = "item-data.json to Product Model"

    def add_arguments(self, parser):
        # hwahae_api/products/fixtures/item-data.json
        parser.add_argument(
            "args", nargs="+", help="input json file",
        )

    def handle(self, *args, **options):

        f = open(*args)
        seeds = json.load(f)

        # 기존 데이터 삭제
        Product.objects.all().delete()

        for seed in seeds:

            category = Category.objects.get_or_create(name=seed["category"])

            product = Product.objects.create(
                id=seed["id"],
                name=seed["name"],
                image_id=seed["imageId"],
                price=seed["price"],
                gender=seed["gender"],
                monthly_sales=seed["monthlySales"],
                category=category[0],
            )

            for ingredient in seed["ingredients"].split(","):
                try:
                    product.ingredients.add(Ingredient.objects.get(name=ingredient))
                except Ingredient.ObjectDoesNotExist:
                    # TODO: log 남기기
                    pass

        self.stdout.write(
            self.style.SUCCESS(f"{Product.objects.count()} products created!")
        )
