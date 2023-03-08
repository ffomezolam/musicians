#!python

from context import sequence

import unittest

class TestMod(unittest.TestCase):
    def test_positive_positive(self):
        self.assertEqual(sequence.mod(5,4), 1)

    def test_negative_positive(self):
        self.assertEqual(sequence.mod(-5,4), -1)

class TestSequence(unittest.TestCase):

    # init

    def setUp(self):
        self.seq = sequence.Sequence()

    def test_init(self):
        with self.subTest("Step count should be 16"):
            self.assertEqual(self.seq.steps, 16)
        with self.subTest("Hit count should be 0"):
            self.assertEqual(self.seq.hits, 0)
        with self.subTest("Data type should be list"):
            self.assertIsInstance(self.seq.seq, list)
        with self.subTest("Data length should be 16"):
            self.assertEqual(len(self.seq.seq), 16)

    # options

    def test_opts(self):
        with self.subTest("Opts should be dict"):
            self.assertIsInstance(self.seq._opts, dict)

        with self.subTest("'relative' opt should exist"):
            self.assertIn('shift-style', self.seq._opts)

        with self.subTest("getopts should return all opts"):
            opts = self.seq.getopts()
            self.assertEqual(opts, self.seq._opts)

        with self.subTest("opts should set option with dict"):
            self.seq.setopts({'shift-style': 'relative'})
            self.assertEqual(self.seq._opts['shift-style'], 'relative')

        with self.subTest("setopts should set option with args"):
            self.seq.setopts('replace-style', 'trim')
            self.assertEqual(self.seq._opts['replace-style'], 'trim')

        with self.subTest("getopts should return a single opt"):
            opt = self.seq.getopts('shift-style')
            self.assertEqual(opt, 'relative')

    # getting contents

    def test_as_list(self):
        self.seq.set([1,2,3])

        self.assertListEqual([1,2,3], self.seq.as_list())

    def test_callable(self):
        self.seq.set([1,2,3])

        self.assertListEqual([1,2,3], self.seq())

    # sequence creation

    def test_set_by_list(self):
        with self.subTest("Should return instance"):
            self.assertIs(self.seq, self.seq.set())

        self.seq.set([1,1,0,0])

        with self.subTest("Step count should be 4"):
            self.assertEqual(self.seq.steps, 4)
        with self.subTest("Hit count should be 2"):
            self.assertEqual(self.seq.hits, 2)
        with self.subTest("Sequence should not change"):
            self.assertEqual(self.seq.as_list(), [1,1,0,0])

    def test_set_default(self):
        dsteps = sequence.DEFAULT_STEPS

        self.seq.set()

        with self.subTest(f"Step count should be {dsteps}"):
            self.assertEqual(self.seq.steps, dsteps)
        with self.subTest("Hit count should be 0"):
            self.assertEqual(self.seq.hits, 0)
        with self.subTest(f"Sequence should be {dsteps} zeros"):
            self.assertListEqual(self.seq.as_list(), [0 for _ in range(dsteps)])

    def test_set_steps(self):
        steps = 4

        self.seq.set(4)

        with self.subTest(f'Step count should be {steps}'):
            self.assertEqual(self.seq.steps, steps)
        with self.subTest("Hit count should be 0"):
            self.assertEqual(self.seq.hits, 0)
        with self.subTest(f'Sequence should be {steps} zeros'):
            self.assertListEqual(self.seq.as_list(), [0 for _ in range(steps)])

    def test_copy(self):
        copy = self.seq.copy()

        with self.subTest("Should return a Sequence instance"):
            self.assertIsInstance(copy, sequence.Sequence)

        with self.subTest("Should contain same list"):
            self.assertListEqual(copy.as_list(), self.seq.as_list())

        with self.subTest("Should contain same options"):
            self.assertDictEqual(copy._opts, self.seq._opts)

    def test_insert(self):
        self.seq.set([1,2,3,4,5])

        with self.subTest("Should insert elements at beat"):
            self.seq.insert([11,21,31], 2)
            self.assertListEqual(self.seq.as_list(), [1,11,21,31,2,3,4,5])

    # sequence manipulation

    def test_remove_one_arg(self):
        self.seq.set([1,2,3,4,5])

        with self.subTest("Should remove from start"):
            self.assertListEqual(self.seq.remove(2).as_list(), [3,4,5])

        with self.subTest("Should remove from end"):
            self.assertListEqual(self.seq.remove(-2).as_list(), [3])

    def test_remove_two_args(self):
        self.seq.set([1,2,3,4,5])

        with self.subTest("Should remove items at beat"):
            self.assertListEqual(self.seq.remove(2,3).as_list(), [1,5])

    def test_append(self):
        self.seq.set([1,2])

        with self.subTest("Should add sequence to end"):
            self.assertListEqual([1,2,3,4], self.seq.append([3,4]).as_list())

    def test_prepend(self):
        self.seq.set([3,4])

        with self.subTest("Should add sequence to start"):
            self.assertListEqual([1,2,3,4], self.seq.prepend([1,2]).as_list())

    def test_replace_in_bounds(self):
        self.seq.set([1,2,3,4])

        with self.subTest("Should replace in bounds"):
            self.assertListEqual([1,5,6,4], self.seq.replace([5,6],2).as_list())

        with self.subTest("Default replacement should be on beat 1"):
            self.assertListEqual([2,3,4,4], self.seq.replace([2,3,4]).as_list())

    def test_replace_with_trim(self):
        self.seq.set([1,2,3,4])
        self.seq.setopts({'replace-style': "trim"})

        self.assertListEqual([1,2,5,6], self.seq.replace([5,6,7], 3).as_list())

    def test_replace_with_expand(self):
        self.seq.set([1,2,3,4])
        self.seq.setopts({'replace-style': 'expand'})

        self.assertListEqual([1,2,5,6,7], self.seq.replace([5,6,7], 3).as_list())

    def test_shift(self):
        with self.subTest("Should return instance"):
            self.assertIs(self.seq, self.seq.shift())

    def test_relative_shift(self):
        self.seq.set([0,1,2,3])
        self.seq.setopts({'shift-style': 'relative'})

        with self.subTest("Sequence should shift forward 1"):
            self.seq.shift(1)
            self.assertEqual(self.seq.as_list(), [3,0,1,2])
            self.assertEqual(self.seq.offset, 1)

        with self.subTest("Sequence should shift forward 2"):
            self.seq.shift(2)
            self.assertEqual(self.seq.as_list(), [1,2,3,0])

        with self.subTest("Sequence should shift back 1"):
            self.seq.shift(-1)
            self.assertEqual(self.seq.as_list(), [2,3,0,1])

        with self.subTest("Sequence should shift back 2"):
            self.seq.shift(-2)
            self.assertEqual(self.seq.as_list(), [0,1,2,3])

        with self.subTest("Sequence should shift forward"):
            self.seq.shift(5)
            self.assertEqual(self.seq.as_list(), [3,0,1,2])

        with self.subTest("Sequence should cycle backward"):
            self.seq.shift(-6)
            self.assertEqual(self.seq.as_list(), [1,2,3,0])

    def test_absolute_shift(self):
        self.seq.set([0,1,2,3])
        self.seq.setopts({'shift-style': 'absolute'})

        with self.subTest("Sequence should shift forward 1 from baseline"):
            self.seq.shift(1)
            self.assertEqual(self.seq.as_list(), [3,0,1,2])

        with self.subTest("Sequence should shift back 1 from baseline"):
            self.seq.shift(-1)
            self.assertEqual(self.seq.as_list(), [1,2,3,0])

    def test_stretch_to(self):
        with self.subTest("It should add zeros to fill"):
            self.seq.set([1,2,3,4])
            self.assertListEqual(self.seq.stretch_to(8).as_list(), [1,0,2,0,3,0,4,0])

        with self.subTest("It should spread original values evenly"):
            self.seq.set([1,2,3,4])
            self.assertListEqual(self.seq.stretch_to(7).as_list(), [1,0,2,0,3,0,4])

        with self.subTest("It should shrink sequence if necessary"):
            self.seq.set([1,2,3,4])
            self.assertListEqual(self.seq.stretch_to(2).as_list(), [1,3])

    def test_stretch_to_with_int(self):
        self.seq.set([1,2,3,4])
        self.seq.setopts('stretch-with', 9)

        with self.subTest("It should add number to fill"):
            self.assertListEqual(self.seq.stretch_to(8).as_list(), [1,9,2,9,3,9,4,9])

    def test_stretch_to_with_repeat(self):
        self.seq.set([1,2,3,4])
        self.seq.setopts('stretch-with', 'repeat')

        with self.subTest("It should repeat stretched items"):
            self.assertListEqual(self.seq.stretch_to(8).as_list(), [1,1,2,2,3,3,4,4])

    def test_stretch_to_with_interpolate(self):
        self.seq.set([1,2,4,8])
        self.seq.setopts('stretch-with', 'interpolate')

        with self.subTest("It should interpolate between items"):
            self.assertListEqual(self.seq.stretch_to(8).as_list(), [1,1.5,2,3,4,6,8,4.5])

        self.seq.set([1,2,4,8])
        with self.subTest("It should repeat last item if specified"):
            self.seq.setopts('interpolate-style', 'repeat')
            self.assertListEqual(self.seq.stretch_to(8).as_list(), [1,1.5,2,3,4,6,8,8])

        self.seq.set([1,2,4,8,10])
        with self.subTest("It should work with uneven length sequences"):
            self.seq.setopts('interpolate-style', 'loop')
            self.assertListEqual(self.seq.stretch_to(8).as_list(), [1,1.5,2,4,6,8,10,5.5])

        with self.subTest("It should work with no replacement at end"):
            self.seq.set([1,2,4,8,10])
            self.assertListEqual(self.seq.stretch_to(7).as_list(), [1,1.5,2,4,6,8,10])

    def test_stretch_by(self):
        with self.subTest("Stretch should be multiple of source length"):
            self.seq.set([1,2,3,4])
            self.seq.setopts('global-rounding', 'auto')

            self.assertListEqual(self.seq.stretch_by(2).as_list(), [1,0,2,0,3,0,4,0])

    def test_shrink_to(self):
        with self.subTest("It should add zeros to fill"):
            self.seq.set([1,2,3,4])
            self.assertListEqual(self.seq.shrink_to(8).as_list(), [1,0,2,0,3,0,4,0])

        with self.subTest("It should shrink sequence if necessary"):
            self.seq.set([1,2,3,4])
            self.assertListEqual(self.seq.shrink_to(2).as_list(), [1,3])

    def test_shrink_by(self):
        with self.subTest("Shrink should be multiple of source length"):
            self.seq.set([1,2,3,4])
            self.assertListEqual(self.seq.shrink_by(2).as_list(), [1,3])

    def test_expand_to(self):
        with self.subTest("It should add zeros to end"):
            self.seq.set([1,2,3,4])
            self.assertListEqual(self.seq.expand_to(6).as_list(), [1,2,3,4,0,0])

    def test_expand_to_with_int(self):
        with self.subTest("It should add int if specified"):
            self.seq.set([1,2])
            self.seq.setopts('expand-with', 5)
            self.assertListEqual(self.seq.expand_to(4).as_list(), [1,2,5,5])

    def test_expand_to_with_repeat(self):
        with self.subTest("It should repeat last value if specified"):
            self.seq.set([1,2,3])
            self.seq.setopts('expand-with', 'repeat')
            self.assertListEqual(self.seq.expand_to(5).as_list(), [1,2,3,3,3])

    def test_expand_to_with_loop(self):
        with self.subTest("It should loop sequence if specified"):
            self.seq.set([1,2,3])
            self.seq.setopts('expand-with', 'loop')
            self.assertListEqual(self.seq.expand_to(8).as_list(), [1,2,3,1,2,3,1,2])

        with self.subTest("It should set loop length by options"):
            self.seq.set([1,2,3])
            self.seq.setopts('expand-with', 'loop-2')
            self.assertListEqual(self.seq.expand_to(8).as_list(), [1,2,3,2,3,2,3,2])

        with self.subTest("It should set loop length by argument"):
            self.seq.set([1,2,3,4])
            self.seq.setopts('expand-with', 'loop-2') # arg should override this
            self.assertListEqual(self.seq.expand_to(8, loop_length=3).as_list(), [1,2,3,4,2,3,4,2])

    def test_expand_to_with_interpolate(self):
        with self.subTest("It should interpolate end to start"):
            self.seq.set([1,5,8,4])
            self.seq.setopts('expand-with', 'interpolate')
            self.assertListEqual(self.seq.expand_to(6).as_list(), [1,5,8,4,3,2])

    def test_expand_by(self):
        with self.subTest("It should expand by multiplier"):
            self.seq.set([1,2,3])
            self.assertListEqual(self.seq.expand_by(3, style='loop-2').as_list(), [1,2,3,2,3,2,3,2,3])

        with self.subTest("It should contract if necessary"):
            self.seq.set([1,2,3,4])
            self.assertListEqual(self.seq.expand_by(0.5).as_list(), [1,2])

    def test_contract_to(self):
        with self.subTest("It should expand if necessary"):
            self.seq.set([1,2])
            self.assertListEqual(self.seq.contract_to(4, 'repeat').as_list(), [1,2,2,2])

        with self.subTest("It should contract if necessary"):
            self.seq.set([1,2,3,4,5,6,7])
            self.assertListEqual(self.seq.contract_to(3, 3).as_list(), [1,2,3])

    def test_contract_by(self):
        with self.subTest("It should expand if necessary"):
            self.seq.set([1,2])
            self.assertListEqual(self.seq.contract_by(0.5, 4).as_list(), [1,2,4,4])

        with self.subTest("It should contract if necessary"):
            self.seq.set([1,2,3,4])
            self.assertListEqual(self.seq.contract_by(2, 'interpolate').as_list(), [1,2])

    def test_reverse(self):
        self.seq.set([1,2,3,4])
        self.assertListEqual(self.seq.reverse().as_list(), [4,3,2,1])

    def test_loop(self):
        with self.subTest("It should loop n times"):
            self.seq.set([1,2,3])
            self.assertListEqual(self.seq.loop(3).as_list(), [1,2,3,1,2,3,1,2,3])

        with self.subTest("It should reverse loop on negative input"):
            self.seq.set([1,2,3])
            self.assertListEqual(self.seq.loop(-3).as_list(), [3,2,1,3,2,1,3,2,1])

    def test_reset(self):
        self.seq.set([1,2,3,4])
        self.seq.expand_to(7)
        with self.subTest("Manipulators should cache original sequence"):
            self.assertListEqual(self.seq.seq, [1,2,3,4,0,0,0])
            self.assertEqual(self.seq._undomgr.size(), 1)

        self.seq.reset()

        with self.subTest("Reset should revert original sequence"):
            self.assertListEqual(self.seq.seq, [1,2,3,4])

        with self.subTest("Reset should erase cache"):
            self.assertEqual(self.seq._undomgr.size("undo"), 0)

    def test_replace_step(self):
        self.seq.set([1,2,3,4])
        self.seq.replace_step(2, 4)
        self.assertSequenceEqual(self.seq.seq, [1,4,3,4])

    def test_remove_step(self):
        with self.subTest("should set to int if style is int"):
            self.seq.set([1,2,3,4])
            self.seq.remove_step(1, 0)
            self.assertSequenceEqual(self.seq.seq, [0,2,3,4])

        with self.subTest("should cut step if style is cut"):
            self.seq.set([1,2,3,4])
            self.seq.remove_step(1, "cut")
            self.assertSequenceEqual(self.seq.seq, [2,3,4])

    def test_replace_value(self):
        self.seq.set([1,2,3,4,3,2,1])
        self.seq.replace_value(2, 5)
        self.assertSequenceEqual(self.seq.seq, [1,5,3,4,3,5,1])

if __name__ == '__main__':
    unittest.main()
