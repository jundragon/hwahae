import json
from django.core.management.base import BaseCommand
from hwahae_api.ingredients.models import Ingredient


class Command(BaseCommand):

    """ hwahae_api/ingredients/fixtures/ingredient-data.json """

    help = "ingredient-data.json to Ingredient Model"

    @staticmethod
    def score(_data):
        if _data == "O":
            return 1
        elif _data == "X":
            return -1
        else:
            return 0

    def add_arguments(self, parser):
        # hwahae_api/products/fixtures/item-data.json
        parser.add_argument(
            "args", nargs="+", help="input json file",
        )

    def handle(self, *args, **options):

        f = open(*args)
        seeds = json.load(f)

        # 기존 데이터 삭제
        # Ingredient.objects.all().delete()

        for seed in seeds:

            Ingredient.objects.create(
                name=seed["name"],
                oily=self.score(seed["oily"]),
                dry=self.score(seed["dry"]),
                sensitive=self.score(seed["sensitive"]),
            )

        self.stdout.write(
            self.style.SUCCESS(f"{Ingredient.objects.count()} ingredients created!")
        )
