from django.db import models
from login.models import Account

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
        s = ", " + self.notes if self.notes!=None else ''
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
        s += 'Cuisines: ' + str(self.cuisines) + '\n'
        s += 'Courses: ' + str(self.courses) + '\n'
        s += 'Ingredients: '  + str(self.ingredients)
        return s

class PantryItem(models.Model):
    item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    owner = models.ForeignKey(Account, related_name = 'pantry', on_delete=models.CASCADE)

    def __str__(self):
        return self.item.name

    class Meta:
        ordering = ('item',)
        unique_together = ('item', 'owner',)
