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
                    self.stdout.write(self.style.SUCCESS('Successfully added recipes from "%s"' %text_file))
            except Exception as e:
                self.stdout.write(str(e) + ' : failed to load recipes from "%s"' %text_file)
                break
        for recipe in recipes:
            r = Recipe()
            r.title = recipe['title']
            r.source = recipe['source']
            r.cuisines = recipe['cuisines']
            r.courses = recipe['courses']
            r.ingredients = recipe['ingredients']
            r.save()
