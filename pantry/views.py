from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *


class FoodItemViewSet(viewsets.ModelViewSet):
    """ ViewSet for viewing and editing Food Item objects """
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
