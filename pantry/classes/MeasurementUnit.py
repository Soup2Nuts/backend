#-------------------------------------------------------------------------------
# Purpose:      Represents an imperial unit of volume, imperial unit of weight, or other unit that is typically used in the United States when cooking
# Author:       K. Hough
# Created:      11/06/2017
#-------------------------------------------------------------------------------
from enum import Enum
from fractions import Fraction
from math import gcd

class MeasurementUnit(Enum):
    #Returns the abbrevaition of the Unit
    def __str__(self):
        return self.value[1]

    #Returns true if unit1 and unit2 are the same type of unit
    def sameUnitType(unit1, unit2):
        return (type(unit1)==type(unit2)) and isinstance(unit1, MeasurementUnit)

    #Returns fratio between unit1 and unit2 as a Fraction objects i.e. unit1.value/unit2.value
    #If unit1 and unit2 are not MeasurementUnit objects or are different types of MeasurementUnit objects throws a TypeError
    def calculateRatio(unit1, unit2):
        if(MeasurementUnit.sameUnitType(unit1, unit2)):
            return Fraction(unit1.value[0], unit2.value[0])
        else:
            raise TypeError("Ratio can only be calculated between two MeasurementUnit objects of the same subclass")

    #returns a unit object if the specified abbreviation matches that of a unit
    #otherwise returns None
    def getUnit(abbreviation):
        for unit in VolumeUnit:
            if unit.value[1] == abbreviation:
                return unit
        for unit in WeightUnit:
            if unit.value[1] == abbreviation:
                return unit
        for unit in OtherUnit:
            if unit.value[1] == abbreviation:
                return unit
        return None

class VolumeUnit(MeasurementUnit):
    TEASPOON = (1, 'tsp')
    TABLESPOON = (3, 'Tbsp')
    CUP = (48, 'C')
    PINT = (96, 'pt')
    QUART = (192, 'qt')
    GALLON = (768, 'gal')

class WeightUnit(MeasurementUnit):
    OUNCE = (1, 'oz')
    POUND = (16, 'lb')

class OtherUnit(MeasurementUnit):
    NO_UNIT = (1, '')
    WHOLE = (1, 'whole')


