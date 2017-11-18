from rest_framework import serializers
from .models import *


class FoodItemSerializer(serializers.ModelSerializer):
    """ Serializer to represent the FoodItem model """
    class Meta:
        model = FoodItem
        fields = ("name",)
