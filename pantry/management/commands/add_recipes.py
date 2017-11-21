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
                    self.stdout.write(self.style.SUCCESS('Successfully loaded "%s". Starting to load recipes...' %text_file))
            except Exception as e:
                self.stdout.write(str(e) + ' : failed to load "%s"' %text_file)
                break
        for recipe in recipes[0:20]:
            r, created = Recipe.objects.get_or_create(title=recipe['title'])
            r.title = recipe['title']
            r.source = recipe['source']
            r.cuisines.clear();
            r.courses.clear();
            r.ingredients.clear();
            r.save()
            for c in recipe['cuisines']:
                cuisine, created = Cuisine.objects.get_or_create(name=str(c))
                cuisine.save()
                r.cuisines.add(cuisine)
            for c in recipe['courses']:
                course, created = Course.objects.get_or_create(name=str(c))
                course.save()
                r.courses.add(course)
            for i in recipe['ingredients']:
                food, created = FoodItem.objects.get_or_create(name=str(i['food']).lower())
                food.save()
                ingred = Ingredient()
                notes = str(i['notes']).lower()
                quantity = str(i['quantity']['fraction'] + ' ' + i['quantity']['unit']).lower()
                # same_ingred = r.ingredients.filter(quantity=quantity, name=food, notes=notes)
                # if(len(same_ingred)==0):  #dont add the ingredient if it is a duplicate
                ingred = Ingredient(quantity=quantity, name=food, notes=notes)
                ingred.save()
                r.ingredients.add(ingred)
            r.save()
            self.stdout.write(self.style.SUCCESS('Successfully loaded recipe: "%s"' %r.title))
