#-------------------------------------------------------------------------------
# Purpose:      Unit tests for the Quantity class
# Author:       K. Hough
# Created:      11/06/2017
#-------------------------------------------------------------------------------
import unittest
from fractions import Fraction
from Quantity import Quantity
from MeasurementUnit import *

class QuantityTest(unittest.TestCase):

    def test_constructor(self):
        q = Quantity(Fraction(1, 3), VolumeUnit.PINT)
        self.assertEqual(q.fraction, Fraction(1, 3))
        self.assertEqual(q.unit, VolumeUnit.PINT)

    def test_mixedNumPrint(self):
        q = Quantity(Fraction(32, 11), VolumeUnit.TEASPOON)
        self.assertEqual(str(q), '2 10/11 tsp')

    def test_Equals(self):
        q = Quantity(Fraction(1, 3), VolumeUnit.PINT)
        self.assertEqual(q, Quantity(Fraction(1, 3), VolumeUnit.PINT))

    def test_adjustUnits(self):
        q = Quantity(Fraction(1, 32), VolumeUnit.PINT)
        q.adjustUnits()
        self.assertEqual(q, Quantity(Fraction(1, 1), VolumeUnit.TABLESPOON))

    def test_multiplyByRatio(self):
        q = Quantity(Fraction(5, 8), VolumeUnit.PINT)
        q.multiplyByRatio(Fraction(4, 9))
        self.assertEqual(q, Quantity(Fraction(5, 18), VolumeUnit.PINT))

if __name__ == '__main__':
    unittest.main()
