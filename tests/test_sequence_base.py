#!python

from context import sequence_base as sequence

import unittest

class TestShift_seq(unittest.TestCase):
    def setUp(self):
        self.seq = [1,2,3,4,5]

    def test_shift(self):
        with self.subTest("Should shift forward"):
            self.assertSequenceEqual(sequence.shift_seq(self.seq, 2), [4,5,1,2,3])
        with self.subTest("Should shift back"):
            self.assertSequenceEqual(sequence.shift_seq(self.seq, -2), [3,4,5,1,2])
        with self.subTest("Should cycle forward"):
            self.assertSequenceEqual(sequence.shift_seq(self.seq, 7), [4,5,1,2,3])
        with self.subTest("Should cycle back"):
            self.assertSequenceEqual(sequence.shift_seq(self.seq, -7), [3,4,5,1,2])

class TestGenerateEuclidean(unittest.TestCase):
    def test_gen(self):
        with self.subTest("Simple division"):
            gen = sequence.generate_euclidean(8, 4, 0)
            expected = [1, 0, 1, 0, 1, 0, 1, 0]
            self.assertListEqual(gen, expected)

        with self.subTest("Tricky division 1"):
            gen = sequence.generate_euclidean(13, 5, 0)
            expected = [1,0,0,1,0,1,0,0,1,0,1,0,0]
            self.assertListEqual(gen, expected)

        with self.subTest("Tricky division 2"):
            gen = sequence.generate_euclidean(12, 5, 0)
            expected = [1,0,0,1,0,1,0,0,1,0,1,0]
            self.assertListEqual(gen, expected)

        with self.subTest("Tricky division 3"):
            gen = sequence.generate_euclidean(24, 11)
            expected = [1,0,0,1,0,1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1,0,1,0]
            self.assertListEqual(gen, expected)

if __name__ == '__main__':
    unittest.main()
