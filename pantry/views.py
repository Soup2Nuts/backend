from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, views, status
from .models import *
from .serializers import *
from rest_framework.decorators import permission_classes, detail_route, list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_decode_handler
from django.core.exceptions import PermissionDenied

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

    #Decode the user from the request's header
    def getUser(request):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            token = token.split(' ', 1)[1]
            user_id = jwt_decode_handler(token)['user_id']
            return User.objects.get(pk=user_id)
        except:
            raise PermissionDenied("Request has an invalid or expired token")

    def list(self, request):
        """
        This view should return a list of all the pantry items
        for the currently authenticated user.
        """
        user = PantryItemViewSet.getUser(request)
        items = user.pantry.all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)

    def put(self, request):
        print(request.data)
        food_name = request.data['food_name']
        #Get the foodItem if it exists
        food = get_object_or_404(FoodItem, pk=food_name)
        user = PantryItemViewSet.getUser(request)
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
        user = PantryItemViewSet.getUser(request)
        items = PantryItem.objects.all().filter(item=food, owner=user.pk)
        if(len(items) <= 0):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        pk = items[0].pk
        item = get_object_or_404(PantryItem, pk=pk)
        if(not(item.owner == user)):
            raise PermissionDenied("You cannot delete pantry item from another user's pantry.")
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
