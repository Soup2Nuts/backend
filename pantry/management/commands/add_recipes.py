# Usage: python manage.py add_recipes pantry/data/recipes2.json
from django.core.management.base import BaseCommand, CommandError
from pantry.models import *
import json

class Command(BaseCommand):
    help = 'Adds recipes to the database from a json file'

    def add_arguments(self, parser):
        parser.add_argument('text_file', nargs='+', type=str)

    def handle(self, *args, **options):
        recipes = []
        for text_file in options['text_file']:
            try:
                with open(text_file, 'r') as f:
                    recipes = json.load(f)
                    self.stdout.write(self.style.SUCCESS('Successfully adding recipes from "%s"' %text_file))
            except Exception as e:
                self.stdout.write(str(e) + ' : failed to load recipes from "%s"' %text_file)
                break
        for recipe in recipes[10:20]:
            r, created = Recipe.objects.get_or_create(title=str(recipe).title())
            r.title = recipe['title']
            r.source = recipe['source']
            r.save()
            for c in recipe['cuisines']:
                cuisine, created = Cuisine.objects.get_or_create(name=str(c).title())
                cuisine.save()
                r.cuisines.add(cuisine)
            for c in recipe['courses']:
                course, created = Course.objects.get_or_create(name=str(c).title())
                course.save()
                r.courses.add(course)
            for i in recipe['ingredients']:
                food, created = FoodItem.objects.get_or_create(name=str(i['food']).lower())
                food.save()
                ingred = Ingredient()
                ingred.notes = str(i['notes']).lower()
                ingred.name = food
                ingred.quantity = str(i['quantity']['fraction'] + ' ' + i['quantity']['unit']).lower()
                ingred.save()
                r.ingredients.add(ingred)
            r.save()
