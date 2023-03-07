#!python

from context import sequence_base as sequence

import unittest

class Test_manipulate_funcs(unittest.TestCase):
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

    def test_stretch(self):
        with self.subTest("Should stretch and fill"):
            self.assertSequenceEqual(sequence.stretch_seq(self.seq, 10, 6),[1,6,2,6,3,6,4,6,5,6])

        with self.subTest("Should stretch and repeat"):
            self.assertSequenceEqual(sequence.stretch_seq(self.seq, 10, "repeat"), [1,1,2,2,3,3,4,4,5,5])

        with self.subTest("Should stretch and interpolate with repeat"):
            self.assertSequenceEqual(sequence.stretch_seq(self.seq, 10, "interpolate", "repeat"), [1,1.5,2,2.5,3,3.5,4,4.5,5,5])

        with self.subTest("Should stretch and interpolate with loop"):
            self.assertSequenceEqual(sequence.stretch_seq(self.seq, 10, "interpolate", "loop"), [1,1.5,2,2.5,3,3.5,4,4.5,5,3])

        with self.subTest("Should stretch and interpolate with repeat and round up"):
            self.assertSequenceEqual(sequence.stretch_seq(self.seq, 10, "interpolate", "repeat", "up"), [1,2,2,3,3,4,4,5,5,5])

        with self.subTest("Should distribute by euclidean algorithm"):
            self.assertSequenceEqual(sequence.stretch_seq(self.seq, 7, 0), [1,0,2,3,0,4,5])

    def test_shrink(self):
        with self.subTest("Should alias stretch"):
            self.assertSequenceEqual(sequence.shrink_seq(self.seq, 10, 6), [1,6,2,6,3,6,4,6,5,6])

        with self.subTest("Should remove items via euclidean algorithm"):
            self.assertSequenceEqual(sequence.shrink_seq(self.seq, 2), [1,3])

        with self.subTest("Should remove items evenly if even"):
            self.assertSequenceEqual(sequence.shrink_seq([1,2,3,4], 2), [1,3])

    def test_expand(self):
        with self.subTest("Should add int at end"):
            self.assertSequenceEqual(sequence.expand_seq(self.seq, 10, 0), [1,2,3,4,5,0,0,0,0,0])

        with self.subTest("Should loop sequence at end"):
            self.assertSequenceEqual(sequence.expand_seq(self.seq, 10, "loop"), [1,2,3,4,5,1,2,3,4,5])

        with self.subTest("Should loop last 3 at end"):
            self.assertSequenceEqual(sequence.expand_seq(self.seq, 10, "loop", 3), [1,2,3,4,5,3,4,5,3,4])

        with self.subTest("Should interpolate to start"):
            self.assertSequenceEqual(sequence.expand_seq(self.seq, 8, "interpolate"), [1,2,3,4,5,4,3,2])

        with self.subTest("Should repeat last value"):
            self.assertSequenceEqual(sequence.expand_seq(self.seq, 7, "repeat"), [1,2,3,4,5,5,5])

    def test_contract(self):
        with self.subTest("Should alias expand"):
            self.assertSequenceEqual(sequence.contract_seq(self.seq, 10, 0), [1,2,3,4,5,0,0,0,0,0])

        with self.subTest("Should trim sequence"):
            self.assertSequenceEqual(sequence.contract_seq(self.seq, 3), [1,2,3])

    def test_reverse(self):
        with self.subTest("Should reverse sequence"):
            self.assertSequenceEqual(sequence.reverse_seq(self.seq), [5,4,3,2,1])

    def test_loop(self):
        with self.subTest("Should loop sequence"):
            self.assertSequenceEqual(sequence.loop_seq(self.seq, 2), [1,2,3,4,5,1,2,3,4,5])

        with self.subTest("Should allow fractional multipliers"):
            self.assertSequenceEqual(sequence.loop_seq(self.seq, 1.5), [1,2,3,4,5,1,2,3])

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
