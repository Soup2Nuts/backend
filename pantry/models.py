from django.db import models

# Create your models here.
class FoodItem(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    quantity = models.CharField(max_length = 50)
    name = models.CharField(max_length = 500)
    notes = models.CharField(max_length = 500)

    def __str__(self):
        s = ", " + self.notes if self.notes!=None else ''
        return self.quantity + ' ' + self.name + s

class Cuisine(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length = 200)
    source = models.URLField(max_length = 200)
    cuisines = models.ManyToManyField(Cuisine)
    courses = models.ManyToManyField(Course)
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        s = 'Title: ' + self.title + '\n'
        s += 'Source: ' + self.source + '\n'
        s += 'Cuisines: ' + str(self.cuisines) + '\n'
        s += 'Courses: ' + str(self.courses) + '\n'
        s += 'Ingredients: '  + str(self.ingredients) + '\n'
        return s
