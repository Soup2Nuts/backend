#-------------------------------------------------------------------------------
# Purpose:      Represents a measured amount
# Author:       K. Hough
# Created:      11/06/2017
#-------------------------------------------------------------------------------
from MeasurementUnit import *
from fractions import Fraction
from math import gcd
class Quantity():

    #Constructor
    def __init__(self, fraction, unit):
        self.fraction = fraction    #Fraction object
        self.unit = unit            #MeasurementUnit object

    def __eq__(self, other):
        if (self.fraction == other.fraction) and (self.unit == other.unit):
            return True
        return False

    # Adjusts the Quantity object's unit to try to minimize the denominator of the Quantity object's fraction
    # Then adjust the object's unit to the largest unit that does not increase the Quantity object's fraction's denominator
    # minimize fraction denom, maximize unit value
    def adjustUnits(self):
            results = []
            for unit in type(self.unit):
                ratio = MeasurementUnit.calculateRatio(self.unit, unit)
                results.append((unit, Fraction(self.fraction*ratio)))
            results.sort(key = lambda el: (el[1].denominator, -el[0].value[0]))
            self.unit = results[0][0]
            self.fraction = results[0][1]

    #Provides meaningful text presentation of Quantity object
    #Represents imporoper fractions as mixed numbers
    def __str__(self):
        #improper frac stuff
        num = self.fraction.numerator
        denom = self.fraction.denominator
        if(num >= denom):
            whole = num//denom
            remainder = num - whole*denom
            s = str(whole)
            s += '' if remainder == 0 else ' ' + str(remainder) + '/' + str(denom)
        else: s = str(self.fraction)
        if str(self.unit) == '':
            return s
        return  s + ' ' + str(self.unit)


    #Multiplies the fractional portion of the Quantity by the specified fraction
    def multiplyByRatio(self, fraction):
        self.fraction = Fraction(self.fraction * fraction)

    #Returns a Fraction object which represents the ratio of the first Quantity object argument
    #to the second Quantity object argument taking their respective units into account
    def getRatio(q1, q2):
        unitRatio = MeasurementUnit.getRatio(q1.unit, q2.unit)
        pass
