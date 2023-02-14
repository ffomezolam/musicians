#!python

from context import opts

import unittest

testopts = {
    "opt1": "value1",
    "opt2": "value2",
    "opt3": "value3",
    "opt4": "value4"
}

class TestGetOpts(unittest.TestCase):
    def test_getopts(self):
        with self.subTest("Should get opt if in opts"):
            self.assertEqual(opts.getopts(testopts, "opt2"), "value2")

        with self.subTest("Should return None if opt not in opts"):
            self.assertIsNone(opts.getopts(testopts, "noneopt"))

        with self.subTest("Should return all opts if no arg"):
            self.assertDictEqual(opts.getopts(testopts), testopts)

class TestSetOpts(unittest.TestCase):
    def test_setopts(self):
        with self.subTest("Should set opt by dict if in opts"):
            self.assertEqual(opts.setopts(testopts, {"opt3": "3val"})['opt3'], "3val")

        with self.subTest("Should set opt by k-v pair if in opts"):
            self.assertEqual(opts.setopts(testopts, "opt1", "babyhead")['opt1'], "babyhead")

        with self.subTest("Should not set opt if not in opts"):
            self.assertNotIn("noneopt", opts.setopts(testopts, "noneopt", "boring"))

        with self.subTest("Should be able to set multiple opts with dict"):
            r = opts.setopts({"opt1": "yoga", "opt4": "demon worship"})
            self.assertEqual(r["opt1"], "yoga")
            self.assertEqual(r["opt4"], "demon worship")

class TestOptsMixin(unittest.TestCase):
    def setUp(self):
        self.opts = opts.OptsMixin(testopts)

    def test_init(self):
        for opt, val in self.opts._opts.items():
            with self.subTest(f"Should have default opt {opt}"):
                self.assertIn(opt, testopts)
                self.assertEqual(val, testopts[opt])

    def test_getopts(self):
        with self.subTest("Should get opt if in opts"):
            self.assertEqual(self.opts.getopts('opt1'), 'value1')

        with self.subTest("Should return None if opt not in opts"):
            self.assertIsNone(self.opts.getopts('opt7'))

        with self.subTest("Should return all opts if no arg"):
            self.assertDictEqual(self.opts.getopts(), testopts)

    def test_setopts(self):
        with self.subTest("Should set opt if in opts"):
            self.opts.setopts({'opt1': 'pastries'})
            self.assertEqual(self.opts._opts['opt1'], 'pastries')

        with self.subTest("Should not set opt if not in opts"):
            self.opts.setopts('opt6', 'balloons')
            self.assertNotIn('opt6', self.opts._opts)

if __name__ == '__main__':
    unittest.main()
