from rest_framework import serializers
from .models import *


class FoodItemSerializer(serializers.ModelSerializer):
    """ Serializer to represent the FoodItem model """
    class Meta:
        model = FoodItem
        fields = ("name",)

class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Recipe model """
    class Meta:
        model = Recipe
        fields = ("title", "source", "cuisines", "courses", "ingredients")

class CourseSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Course model """
    class Meta:
        model = Course
        fields = ("name", )

class CuisineSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Cuisine model """
    class Meta:
        model = Cuisine
        fields = ("name", )
