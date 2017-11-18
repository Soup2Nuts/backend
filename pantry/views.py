from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *


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
