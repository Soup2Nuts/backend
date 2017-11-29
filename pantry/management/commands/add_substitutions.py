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
            valid_sub = True
            if(len(sub[0].strip())==0 or sub[0].strip()=='egg' or 'large egg' in sub[0].strip()):
                valid_sub = False
                break
            original_food, created = FoodItem.objects.get_or_create(pk=sub[0].strip())
            sub_foods = []
            sub_ratios = []
            for sf in sub[1]:
                if(len(sf[0].strip())<=0):
                    valid_sub = False
                    break
                sub_ratios.append(sf[0].strip())
                name = sf[1].strip()
                if(len(name)<=0):
                    valid_sub = False
                    break
                sub_food, created = FoodItem.objects.get_or_create(pk=name)
                sub_foods.append(sub_food)
            if(valid_sub):
                sub_obj = Substitution(original_food=original_food)
                sub_obj.save()
                for i in range(0, len(sub_foods)):
                                sub_food_obj = SubstituteFood(substitute_food=sub_foods[i], ratio=sub_ratios[i], substitution=sub_obj)
                                sub_food_obj.save()
                self.stdout.write(self.style.SUCCESS('Successfully loaded substitution: \n"%s"' %sub_obj))
