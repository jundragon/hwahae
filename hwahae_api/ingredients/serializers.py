from rest_framework import serializers
from .models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):

    """ Ingredient Serializer Definition """

    def to_representation(self, value):
        return value.name

    class Meta:
        model = Ingredient
        fields = ("name",)
