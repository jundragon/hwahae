from rest_framework import serializers
from hwahae_api.ingredients.serializers import IngredientSerializer
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):

    """ Category Serializer Definition """

    class Meta:
        model = Category
        exclude = (
            "id",
            "created",
            "updated",
        )


class ProductSerializer(serializers.ModelSerializer):

    """ Product Serializer Definition """

    ingredients = IngredientSerializer(read_only=True, many=True)
    monthlySales = serializers.IntegerField(source="monthly_sales")
    category = CategorySerializer()

    def to_representation(self, instance):
        # ingredients 를 리스트가 아닌 string으로 반환하기 위함
        representation = super().to_representation(instance)
        ingredients = representation.pop("ingredients")
        representation["ingredients"] = ",".join(ingredients)
        return representation

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "ingredients",
            "monthlySales",
            "score_oily",
            "score_dry",
            "score_sensitive",
            "category",
        )
