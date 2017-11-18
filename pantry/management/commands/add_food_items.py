#Use python manage.py add_food_items pantry/data/food_items.txt
from django.core.management.base import BaseCommand, CommandError
from pantry.models import *

class Command(BaseCommand):
    help = 'Adds food item strings from text files'

    def add_arguments(self, parser):
        parser.add_argument('text_file', nargs='+', type=str)

    def handle(self, *args, **options):
        for text_file in options['text_file']:
            try:
                with open(text_file, 'r') as file:
                    for line in file:
                        item = FoodItem()
                        item.name = line.strip()
                        item.save()
                self.stdout.write(self.style.SUCCESS('Successfully added food from "%s"' % text_file))
            except OSError:
                self.stdout.write('Failed to open file "%s"' % text_file)
