#-------------------------------------------------------------------------------
# Purpose:
# Author:       K. Hough
# Date:         11/07/17
#-------------------------------------------------------------------------------
class Ingredient():

    def __init__(self, quantity = None, food = None, notes = None):
        self.quantity = quantity
        self.food = food
        self.notes  = '' if None else notes

    def __str__(self):
        notes = '' if (self.notes in [None, '', ' ']) else ' ' + '(' + str(self.notes) + ')'
        return str(self.quantity) + ' ' + str(self.food) + notes


