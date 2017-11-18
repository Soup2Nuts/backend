#-------------------------------------------------------------------------------
# Purpose:      Unit tests for the MeasurementUnit class and its subclasses
# Author:       K. Hough
# Created:      11/06/2017
#-------------------------------------------------------------------------------
import unittest
from fractions import Fraction
from MeasurementUnit import *

class MeasurementUnitTest(unittest.TestCase):

    def test_getRatio1(self):
        unit1 = VolumeUnit.PINT
        unit2 = VolumeUnit.TABLESPOON
        fraction = VolumeUnit.calculateRatio(unit1, unit2)
        self.assertEqual(fraction, Fraction(32, 1))

    def test_getRatio2(self):
        unit1 = VolumeUnit.QUART
        unit2 = VolumeUnit.GALLON
        fraction = VolumeUnit.calculateRatio(unit1, unit2)
        self.assertEqual(fraction, Fraction(1, 4))

    def test_getRatioException1(self):
        unit1 = VolumeUnit.GALLON
        unit2 = 'Cup'
        self.assertRaises(Exception, VolumeUnit.calculateRatio, unit1, unit2)

    def test_getRatioException2(self):
        unit1 = VolumeUnit.GALLON
        unit2 = WeightUnit.OUNCE
        self.assertRaises(Exception, VolumeUnit.calculateRatio, unit1, unit2)

    def test_toString1(self):
        unit1 = WeightUnit.OUNCE
        self.assertEqual('oz', str(unit1))

    def test_toString2(self):
        unit1 = VolumeUnit.QUART
        self.assertEqual('qt', str(unit1))

    def test_getUnit1(self):
        self.assertEqual(VolumeUnit.GALLON, MeasurementUnit.getUnit('gal'))

    def test_getUnit1(self):
        self.assertEqual(None, MeasurementUnit.getUnit('pancake'))

if __name__ == '__main__':
    unittest.main()
