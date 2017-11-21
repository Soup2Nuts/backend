from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, views, status
from .models import *
from .serializers import *
from rest_framework.decorators import permission_classes, detail_route, list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_decode_handler

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

class PantryItemViewSet(viewsets.ViewSet):
    """ ViewSet for viewing and editing PantryItem objects """
    serializer_class = PantryItemSerializer
    def list(self, request):
        """
        This view should return a list of all the pantry items
        for the currently authenticated user.
        """
        token = request.META['HTTP_AUTHORIZATION']
        token = token.split(' ', 1)[1]
        print(token)
        user_id = jwt_decode_handler(token)['user_id']
        print(user_id)
        user = User.objects.get(user_id)
        items = user.pantry.all()
        print(items)
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)
