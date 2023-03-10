#!python

from context import duration as d

import unittest
from fractions import Fraction
from math import floor, ceil

class Test_helpers(unittest.TestCase):
    def test_validate_dur(self):
        self.assertRaises(ValueError, d.validate_dur, '3n')
        self.assertEqual('4n', d.validate_dur(4))

    def test_split_dur(self):
        self.assertSequenceEqual(d.split_dur('4t'), ('4', 't'))

    def test_dur_to_frac(self):
        self.assertEqual(d.dur_to_frac('4d'), Fraction(3, 8))

    def test_frac_to_dur(self):
        with self.subTest("Should return fraction if note is simple"):
            self.assertEqual(d.frac_to_dur(Fraction(3, 8)), '4d')

        with self.subTest("Should return tuple if note is complex"):
            self.assertSequenceEqual(d.frac_to_dur(Fraction(7, 8)), ('2n', '4d'))

    def add_durs(self):
        self.assertEqual(d.add_durs('4n', '4n'), '2n')

    def sub_durs(self):
        self.assertEqual(d.sub_durs('2n', '4n'), '4n')

    def mul_dur(self):
        self.assertEqual(d.mul_dur('2n', 2), '1n')

    def div_dur(self):
        self.assertEqual(d.div_dur('2n', 2), '4n')

class Test_Duration(unittest.TestCase):
    def setUp(self):
        self.D = d.Duration('4n')

    def test_set(self):
        self.D.set('8d')
        self.assertEqual(self.D.duration, '8d')

    def test_equality(self):
        od = d.Duration('8d')
        self.D.set('4d')

        with self.subTest("Duration equality"):
            self.assertNotEqual(self.D, od)
            self.D.set('8d')
            self.assertEqual(self.D, od)

        with self.subTest("String equality"):
            self.assertEqual(self.D, '8d')

        with self.subTest("Integer equality"):
            self.D.set('4n')
            self.assertEqual(self.D, 4)

        with self.subTest("Fraction equality"):
            self.D.set('4n')
            self.assertEqual(self.D, Fraction(1, 4))

    def test_addition(self):
        self.D.set('4n')

        with self.subTest("Integer addition"):
            self.assertEqual(self.D + 4, d.Duration('2n'))

        with self.subTest("String addition"):
            self.assertEqual(self.D + '4n', d.Duration('2n'))

        with self.subTest("Duration addition"):
            self.assertEqual(self.D + d.Duration('4n'), d.Duration('2n'))

        with self.subTest("Fraction addition"):
            self.assertEqual(self.D + Fraction(1,4), d.Duration(2))

        with self.subTest("Large value output should be tuple"):
            self.D.set('1n')
            self.assertSequenceEqual(self.D + 4, (d.Duration(1), d.Duration(4)))

    def test_subtraction(self):
        self.D.set('2d')

        with self.subTest("Integer subtraction"):
            self.assertEqual(self.D - 4, d.Duration('2n'))

        with self.subTest("String subtraction"):
            self.assertEqual(self.D - '4n', d.Duration('2n'))

        with self.subTest("Duration subtraction"):
            self.assertEqual(self.D - d.Duration('4n'), d.Duration('2n'))

        with self.subTest("Fraction subtraction"):
            self.assertEqual(self.D - Fraction(1,4), d.Duration(2))

    def test_multiplication(self):
        self.D.set('4n')

        self.assertEqual(self.D * 4, '1n')

    def test_division(self):
        self.D.set('4n')

        self.assertEqual(self.D / 2, '8n')

    def test_inplace_addition(self):
        self.D.set('2n')
        self.D += 2

        self.assertEqual(self.D, 1)

    def test_inplace_subtraction(self):
        self.D.set('2n')
        self.D -= 2

        self.assertEqual(self.D, 4)

    def test_inplace_multiplication(self):
        self.D.set('2n')
        self.D *= 2

        self.assertEqual(self.D, 1)

    def test_inplace_division(self):
        self.D.set('2n')
        self.D /= 2

        self.assertEqual(self.D, 4)

    def test_round(self):
        self.D.set('2d')

        self.assertEqual(round(self.D), 2)

    def test_floor(self):
        self.D.set('2d')

        self.assertEqual(floor(self.D), 2)

    def test_ceil(self):
        self.D.set('2d')

        self.assertEqual(ceil(self.D), 1)

if __name__ == '__main__':
    unittest.main()
