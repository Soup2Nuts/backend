from django.db import models

# Create your models here.
class FoodItem(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length = 200)
    source = models.URLField(max_length = 200)
    cuisines = models.CharField(max_length = 500)
    courses = models.CharField(max_length = 500)
    ingredients = models.CharField(max_length = 20000)

    def __str__(self):
        s = 'Title: ' + self.title + '\n'
        s += 'Source: ' + self.source + '\n'
        s += 'Cuisines: ' + str(self.cuisines) + '\n'
        s += 'Courses: ' + str(self.courses) + '\n'
        s += 'Ingredients:\n'
        for ingredient in self.ingredients.split(', '):
            s+= str(ingredient) + '\n'
        return s
