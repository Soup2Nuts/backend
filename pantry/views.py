from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, views
from .models import *
from .serializers import *
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .permissions import IsPantryItemOwner

@permission_classes((permissions.IsAuthenticated, ))
class FoodItemViewSet(viewsets.ModelViewSet):
    """ ViewSet for viewing and editing Food Item objects """
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer

@permission_classes((permissions.IsAuthenticated, ))
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

class PantryItemViewSet(viewsets.ModelViewSet):
    """ ViewSet for viewing and editing PantryItem objects """
    serializer_class = PantryItemSerializer
    permission_classes = (permissions.IsAuthenticated, IsPantryItemOwner)

    def get_queryset(self):
        """
        This view should return a list of all the pantry items
        for the currently authenticated user.
        """
        user = self.request.user
        queryset = PantryItem.objects.filter(owner=user)
        #self.check_object_permissions(self.request, queryset)
        return queryset
