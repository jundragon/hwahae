from django.conf import settings
from rest_framework import serializers
from hwahae_api.ingredients.serializers import IngredientSerializer
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):

    """ Category Serializer Definition """

    def to_representation(self, instance):
        return instance.name

    class Meta:
        model = Category
        fields = ("name",)


class ProductSerializer(serializers.ModelSerializer):

    """ Product Serializer Definition """

    ingredients = IngredientSerializer(read_only=True, many=True)
    monthlySales = serializers.IntegerField(source="monthly_sales")
    imgUrl = serializers.SerializerMethodField()

    def to_representation(self, instance):
        # ingredients 를 리스트가 아닌 string으로 반환하기 위함
        representation = super().to_representation(instance)
        ingredients = representation.pop("ingredients")
        representation["ingredients"] = ",".join(ingredients)

        return representation

    def get_imgUrl(self, obj):
        thumbnail_url = getattr(settings, "THUMBNAIL_IMAGE_URL")
        return f"{thumbnail_url}/{obj.image_id}.jpg"

    class Meta:
        model = Product
        fields = (
            "id",
            "imgUrl",
            "name",
            "price",
            "ingredients",
            "monthlySales",
            # "score_oily",
            # "score_dry",
            # "score_sensitive",
        )


class ProductDetailSerializer(serializers.ModelSerializer):

    """ Product Detail Serializer Definition """

    ingredients = IngredientSerializer(read_only=True, many=True)
    monthlySales = serializers.IntegerField(source="monthly_sales")
    category = CategorySerializer(read_only=True)
    imgUrl = serializers.SerializerMethodField()

    def to_representation(self, instance):
        # ingredients 를 리스트가 아닌 string으로 반환하기 위함
        representation = super().to_representation(instance)
        ingredients = representation.pop("ingredients")
        representation["ingredients"] = ",".join(ingredients)

        return representation

    def get_imgUrl(self, obj):
        thumbnail_url = getattr(settings, "THUMBNAIL_IMAGE_URL")
        return f"{thumbnail_url}/{obj.image_id}.jpg"

    class Meta:
        model = Product
        fields = (
            "id",
            "imgUrl",
            "name",
            "price",
            "gender",
            "category",
            "ingredients",
            "monthlySales",
            # "score_oily",
            # "score_dry",
            # "score_sensitive",
        )
