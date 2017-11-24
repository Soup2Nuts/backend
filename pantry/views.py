from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, views, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.forms import model_to_dict
from .utils import *
from .models import *
from .serializers import *
import json

@api_view(['GET'])
def search_recipes(request, format=None):
    user = get_user(request)
    # user = User.objects.all()[0]
    try:
        cuisines = request.data['cuisines']
    except:
        cuisines = None
    try:
        courses = request.data['courses']
    except:
        courses = None
    recipes = get_all_valid_recipes(user, cuisines, courses)
    value = []
    for recipe in recipes:
        recipe_serializer = RecipeSerializer(recipe)
        recipe_dict = dict(recipe_serializer.data)
        recipe_dict['substitutions'] =  get_real_substitutions(get_substitutions_made(user, recipe), recipe_dict['ingredients'])
        recipe_dict['numberOfSubstitutions'] = len(recipe_dict['substitutions'])
        value.append(recipe_dict)
    return JsonResponse({'value':value})

class FoodItemViewSet(viewsets.ModelViewSet):
    """ ViewSet for viewing and editing Food Item objects """
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    """ ViewSet for viewing and editing Recipe objects """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class CourseViewSet(viewsets.ModelViewSet):
    """ ViewSet for viewing and editing Course objects """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CuisineViewSet(viewsets.ModelViewSet):
    """ ViewSet for viewing and editing Cuisine objects """
    queryset = Cuisine.objects.all()
    serializer_class = CuisineSerializer

class SubstitutionViewSet(viewsets.ModelViewSet):
    """ ViewSet for viewing and editing Substitution objects """
    queryset = Substitution.objects.all()
    serializer_class = SubstitutionSerializer

class SubstituteFoodViewSet(viewsets.ModelViewSet):
    """ ViewSet for viewing and editing Substitution objects """
    queryset = SubstituteFood.objects.all()
    serializer_class = SubstituteFoodSerializer

class PantryItemViewSet(viewsets.ViewSet):
    """ ViewSet for viewing and editing PantryItem objects """
    serializer_class = PantryItemSerializer

    def list(self, request):
        """
        This view should return a list of all the pantry items
        for the currently authenticated user.
        """
        user = get_user(request)
        items = user.pantry.all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)

    def put(self, request):
        food_name = request.data['food_name']
        #Get the foodItem if it exists
        food = get_object_or_404(FoodItem, pk=food_name)
        user = get_user(request)
        serializer = self.serializer_class(data={'item':food, 'owner':user.pk })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        food_name = request.META['QUERY_STRING']
        food_name = food_name.split('=', 1)[1]
        food_name = food_name.replace("+", " ")
        food = get_object_or_404(FoodItem, pk=food_name)
        user = get_user(request)
        items = PantryItem.objects.all().filter(item=food, owner=user.pk)
        if(len(items) <= 0):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        pk = items[0].pk
        item = get_object_or_404(PantryItem, pk=pk)
        if(not(item.owner == user)):
            raise PermissionDenied("You cannot delete pantry item from another user's pantry.")
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FavoriteRecipeViewSet(viewsets.ViewSet):
    """ ViewSet for viewing and editing FavoriteRecipe objects """
    serializer_class = FavoriteRecipeSerializer

    def list(self, request):
        """
        This view should return a list of all the favorite recipes
        for the currently authenticated user.
        """
        user = get_user(request)
        items = user.favorites.all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)

    def put(self, request):
        recipe_name = request.data['recipe_name']
        #Get the Recipe if it exists
        recipe = get_object_or_404(Recipe, pk=recipe_name)
        user = get_user(request)
        new_fav = FavoriteRecipe(recipe=recipe, owner=user)
        if new_fav:
            new_fav.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        recipe_name = request.META['QUERY_STRING']
        recipe_name = recipe_name.split('=', 1)[1]
        recipe_name = recipe_name.replace("+", " ")
        recipe = get_object_or_404(Recipe, pk=recipe_name)
        user = get_user(request)
        recipes = FavoriteRecipe.objects.all().filter(recipe=recipe, owner=user.pk)
        if(len(recipes) <= 0):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        recipe = recipes[0]
        # recipe = get_object_or_404(Recipe, pk=pk)
        if(not(recipe.owner == user)):
            raise PermissionDenied("You cannot delete another user's favorites.")
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
