#!python

from context import helpers

import unittest

class TestMod(unittest.TestCase):
    def test_positive_positive(self):
        self.assertEqual(helpers.mod(5,4), 1)

    def test_negative_positive(self):
        self.assertEqual(helpers.mod(-5,4), -1)

class TestRounders(unittest.TestCase):
    def test_auto(self):
        with self.subTest("Should round up at 0.5"):
            self.assertEqual(helpers.rounder(0.5, "auto"), 1)

        with self.subTest("Should round down below 0.5"):
            self.assertEqual(helpers.rounder(0.4, "auto"), 0)

    def test_up(self):
        self.assertEqual(helpers.rounder(0.4, "up"), 1)

    def test_down(self):
        self.assertEqual(helpers.rounder(0.9, "down"), 0)

class TestInterpolate(unittest.TestCase):
    def test_interpolate(self):
        with self.subTest("Should interpolate linearly between values"):
            with self.subTest("Single intermediate"):
                self.assertListEqual(helpers.interpolate(2,4),[3])
            with self.subTest("Multiple intermediates"):
                self.assertListEqual(helpers.interpolate(2,5,2),[3,4])

if __name__ == '__main__':
    unittest.main()
