from rest_framework import serializers
from .models import *

class FoodItemSerializer(serializers.ModelSerializer):
    """ Serializer to represent the FoodItem model """
    class Meta:
        model = FoodItem
        fields = ("name",)

class CourseSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Course model """
    class Meta:
        model = Course
        fields = ("name", )

class SubstitutionSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Substitution model """
    class Meta:
        model = Substitution
        fields = ("original_food", "substitute_foods")

class SubstituteFoodSerializer(serializers.ModelSerializer):
    """ Serializer to represent the SubstituteFood model """
    class Meta:
        model = SubstituteFood
        fields = ("ratio", "substitute_food", "substitution")

class CuisineSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Cuisine model """
    class Meta:
        model = Cuisine
        fields = ("name", )

class IngredientSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Ingredient model """
    class Meta:
        model = Ingredient
        fields = ("quantity", "name", "notes")

class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer to represent the Recipe model """
    ingredients = IngredientSerializer(many=True)
    class Meta:
        model = Recipe
        fields = ("title", "source", "cuisines", "courses", "ingredients")

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients_data:
          ingredient, created = Ingredient.objects.get_or_create(name=ingredient['name'])
          recipe.ingredients.add(ingredient)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        instance.name = validated_data['name']
        instance.source = validated_data['source']
        instance.cuisines = validated_data['cuisines']
        instance.courses = validated_data['courses']
        for ingredient in ingredients_data:
            ingredient, created = Ingredient.objects.get_or_create(name=ingredient['name'])
            recipe.ingredients.add(ingredient)
        return instance

class PantryItemSerializer(serializers.ModelSerializer):
    """ Serializer to represent the PantryItem model """

    class Meta:
        model = PantryItem
        fields = ("item", "owner")

    def create(self, validated_data):
    	return PantryItem.objects.create(**validated_data)

class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """ Serializer to represent the FavoriteRecipe model """
    recipe = RecipeSerializer(required=True)
    class Meta:
        model = FavoriteRecipe
        fields = ("recipe", "owner")

    def create(self, validated_data):
        recipe_data = validated_data.pop('recipe', None)
        recipe = Recipe.objects.create_recipe(**recipe_data)
        return FavoriteRecipe.objects.create(recipe=recipe, **validated_data)
