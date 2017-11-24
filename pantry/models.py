from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class FoodItem(models.Model):
    #primary key field is read-only, trying to change the primary_key field will create a new object
    name = models.CharField(max_length = 200, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Course(models.Model):
    #primary key field is read-only, trying to change the primary_key field will create a new object
    name = models.CharField(max_length = 200, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Ingredient(models.Model):
    quantity = models.CharField(max_length = 50)
    name = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    notes = models.CharField(max_length = 500, null=True, blank=True)

    def __str__(self):
        s = (", " + self.notes) if (self.notes!=None and len(self.notes) > 0) else ''
        return self.quantity + ' ' + self.name.name + s

class Cuisine(models.Model):
    #primary key field is read-only, trying to change the primary_key field will create a new object
    name = models.CharField(max_length = 200, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Recipe(models.Model):
    #primary key field is read-only, trying to change the primary_key field will create a new object
    title = models.CharField(max_length = 200, primary_key=True)
    source = models.URLField(max_length = 500, blank=True)
    cuisines = models.ManyToManyField(Cuisine, blank=True)
    courses = models.ManyToManyField(Course, blank=True)
    ingredients = models.ManyToManyField(Ingredient, blank=True)

    def __str__(self):
        s = 'Title: ' + self.title + '\n'
        s += 'Source: ' + self.source + '\n'
        s += 'Cuisines: ' + str(self.cuisines.all()) + '\n'
        s += 'Courses: ' + str(self.courses.all()) + '\n'
        s += 'Ingredients: '  + str(self.ingredients.all())
        return s

    class Meta:
        ordering = ('title',)

class PantryItem(models.Model):
    item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name = 'pantry', on_delete=models.CASCADE)

    def __str__(self):
        return self.item.name

    class Meta:
        ordering = ('item',)
        unique_together = ('item', 'owner',)

class FavoriteRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name = 'favorites', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.recipe)

    class Meta:
        ordering = ('recipe',)
        unique_together = ('recipe', 'owner',)

class Substitution(models.Model):
    original_food = models.ForeignKey(FoodItem, related_name='substitutions', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.original_food) + ': ' + str(self.substitute_foods.all())

    class Meta:
        ordering = ('original_food',)

class SubstituteFood(models.Model):
    substitute_food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    ratio = models.CharField(max_length = 200)
    substitution = models.ForeignKey(Substitution, related_name='substitute_foods', on_delete=models.CASCADE)

    def __str__(self):
        return self.ratio + ' ' + str(self.substitute_food)

    class Meta:
        ordering = ('substitute_food',)
        unique_together = ('substitute_food', 'substitution',)
