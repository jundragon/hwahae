from django.conf import settings
from rest_framework import serializers
from .models import Product


class BaseProductSerializer(serializers.ModelSerializer):
    """
    Base Product Serializer Definition
    """

    ingredients = serializers.StringRelatedField(many=True)
    monthlySales = serializers.IntegerField(source="monthly_sales")
    imgUrl = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()

    def get_imgUrl(self, obj):
        thumbnail_url = getattr(settings, "THUMBNAIL_IMAGE_URL")
        return f"{thumbnail_url}/{obj.image_id}.jpg"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # ingredients 를 리스트가 아닌 string으로 반환하기 위함
        if "ingredients" in representation.keys():
            ingredients = representation.pop("ingredients")
            representation["ingredients"] = ",".join(ingredients)

        return representation


class ProductSerializer(BaseProductSerializer):

    """
    Product Serializer Definition
    """

    class Meta:
        model = Product
        fields = (
            "id",
            "imgUrl",
            "name",
            "price",
            "ingredients",
            "monthlySales",
        )


class ProductDetailSerializer(BaseProductSerializer):

    """
    Product Detail Serializer Definition
    """

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
        )


class ProductRecommendSerializer(BaseProductSerializer):

    """ Product Detail Serializer Definition """

    class Meta:
        model = Product
        fields = (
            "id",
            "imgUrl",
            "name",
            "price",
        )
