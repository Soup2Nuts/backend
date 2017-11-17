from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from backend.serializers import UserSerializer, GroupSerializer, IngredientSerializer
from .models import Ingredient

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ingredients to be viewed or edited
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer