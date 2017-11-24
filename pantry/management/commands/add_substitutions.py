# Usage: python manage.py add_substitutions pantry/data/substitutions.pickle
# Note: Do not run this command more than once on the database as this command does not check that substitutions aren't already in the database before adding them
from django.core.management.base import BaseCommand, CommandError
from pantry.models import *
import pickle

class Command(BaseCommand):
    help = 'Adds substitution to the database from a file of pickled python objects'

    def add_arguments(self, parser):
        parser.add_argument('text_file', nargs='+', type=str)

    def handle(self, *args, **options):
        substitutions = []
        for text_file in options['text_file']:
            try:
                with open(text_file, 'rb') as f:
                    substitutions = pickle.load(f)
                    self.stdout.write(self.style.SUCCESS('Successfully loaded "%s". Starting to load substitutions...' %text_file))
            except Exception as e:
                self.stdout.write(str(e) + ' : failed to load "%s"' %text_file)
                break
        for sub in substitutions:
            print(sub)
            original_food, created = FoodItem.objects.get_or_create(pk=sub[0])
            sub_obj = Substitution(original_food=original_food)
            sub_obj.save()
            for sf in sub[1]:
                ratio = sf[0]
                sub_food, created = FoodItem.objects.get_or_create(pk=sf[1])
                sub_food_obj = SubstituteFood(substitute_food=sub_food, ratio=ratio, substitution=sub_obj)
                sub_food_obj.save()
            self.stdout.write(self.style.SUCCESS('Successfully loaded substitution: "%s"' %sub_obj))
