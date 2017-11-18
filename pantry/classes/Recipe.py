#-------------------------------------------------------------------------------
# Purpose:      Represents a recipe for preparing food
# Author:       K. Hough
#-------------------------------------------------------------------------------

class Recipe():

    def __init__(self, title=None , source=None, prepTime=None, cookTime=None, cuisines=None, courses=None, ingredients=None):
        self.title = '' if title == None else title
        self.source = '' if source == None else source
        self.cuisines = [] if cuisines == None else cuisines
        self.courses = [] if courses == None else courses
        self.ingredients = [] if ingredients == None else ingredients

    def __str__(self):
        s = 'Title: ' + self.title + '\n'
        s += 'Source: ' + self.source + '\n'
        s += 'Cuisines: ' + str(self.cuisines) + '\n'
        s += 'Courses: ' + str(self.courses) + '\n'
        s += 'Ingredients:\n'
        for ingredient in self.ingredients:
            s+= str(ingredient) + '\n'
        return s
