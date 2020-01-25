from rest_framework import serializers
from .models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):

    """ Ingredient Serializer Definition """

    class Meta:
        model = Ingredient
        fields = ("name",)
