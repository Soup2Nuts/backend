from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(FoodItem)
admin.site.register(Recipe)
admin.site.register(Course)
admin.site.register(Cuisine)
admin.site.register(Ingredient)
admin.site.register(PantryItem)
admin.site.register(FavoriteRecipe)
admin.site.register(Substitution)
admin.site.register(SubstituteFood)
