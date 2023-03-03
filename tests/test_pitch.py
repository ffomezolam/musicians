#!python

from context import pitch as p

import unittest

class TestRE_PITCH(unittest.TestCase):
    def setUp(self):
        self.re = p.RE_PITCH

    def test_re(self):
        with self.subTest("Should not match non-notes"):
            self.assertIsNone(self.re.match('Z'))
            self.assertIsNone(self.re.match('Z#1'))
        with self.subTest("Should not match accidental only"):
            self.assertIsNone(self.re.match('#'))
        with self.subTest("Should not match octave only"):
            self.assertIsNone(self.re.match('-1'))
        with self.subTest("Should match note name only"):
            self.assertTrue(self.re.match('C'))
            self.assertTupleEqual(self.re.match('D').groups(), ('D', '', None))
        with self.subTest("Should not match note name with improper accidental"):
            self.assertIsNone(self.re.match('Cz'))
        for a in ['#','s','b']:
            with self.subTest(f"Should match note name and accidental {a}"):
                self.assertTrue(self.re.match(f'C{a}'))
                self.assertTupleEqual(self.re.match(f'D{a}').groups(), ('D', a, None))
        with self.subTest("Should match note name and octave"):
            self.assertTrue(self.re.match('C1'))
            self.assertTupleEqual(self.re.match(f'E5').groups(), ('E', '', '5'))
        with self.subTest("Should match note name, accidental, and octave"):
            self.assertTrue(self.re.match('Gb1'))
            self.assertTupleEqual(self.re.match('A##4').groups(), ('A','##','4'))

class Test_format_accidental(unittest.TestCase):
    def test_note(self):
        self.assertEqual(p.format_accidental('C#2'), 'Cs2')
        self.assertEqual(p.format_accidental('Db'), 'Db')

    def test_accidental(self):
        self.assertEqual(p.format_accidental('#'), 's')
        self.assertEqual(p.format_accidental('s'), 's')

    def test_non_conformant(self):
        self.assertEqual(p.format_accidental('Z#10'), 's')
        self.assertEqual(p.format_accidental('ZhK'), '')

    def test_humanize(self):
        self.assertEqual(p.format_accidental('Cs2', 'symbol'), 'C#2')
        self.assertEqual(p.format_accidental('s', 'symbol'), '#')

class TestOffset_to_note(unittest.TestCase):
    def test_positive(self):
        with self.subTest("Offset 2 should be D"):
            self.assertEqual(p.offset_to_note(2), 'D')
        with self.subTest("Offset 16 should be E"):
            self.assertEqual(p.offset_to_note(16), 'E')

    def test_negative(self):
        with self.subTest("Offset -1 should be B"):
            self.assertEqual(p.offset_to_note(-1), 'B')
        with self.subTest("Offset -15 should be A"):
            self.assertEqual(p.offset_to_note(-15), 'A')

    def test_accidental(self):
        with self.subTest("Should pick flat if lean < 0"):
            self.assertEqual(p.offset_to_note(1, -1), 'Db')

        with self.subTest("Should pick sharp if lean > 0"):
            self.assertEqual(p.offset_to_note(1, 1), 'Cs')

class TestNote_to_offset(unittest.TestCase):
    def test_conformant(self):
        self.assertEqual(p.note_to_offset('Cs'), 1)
        self.assertEqual(p.note_to_offset('Db'), 1)
        self.assertEqual(p.note_to_offset('A'), 9)

class Testparse_pitch(unittest.TestCase):
    def test(self):
        self.assertTupleEqual(p.parse_pitch('Gb3'), ('G', 'b', 3))
        self.assertTupleEqual(p.parse_pitch('D#2'), ('D', 's', 2))

class TestPitch_to_value(unittest.TestCase):
    def test_default_octave(self):
        self.assertEqual(p.pitch_to_value('D#5'), 75)
        self.assertEqual(p.pitch_to_value('A2'), 45)
        self.assertEqual(p.pitch_to_value('D',5), 74)

    def test_custom_octave(self):
        self.assertEqual(p.pitch_to_value('D#5', middle_c_octave = 3), 87)

class TestValue_to_pitch(unittest.TestCase):
    def test_default_octave(self):
        self.assertEqual(p.value_to_pitch(75), 'Ds5')
        self.assertEqual(p.value_to_pitch(45), 'A2')

    def test_custom_octave(self):
        self.assertEqual(p.value_to_pitch(87, middle_c_octave = 3), 'Ds5')

class TestPitch(unittest.TestCase):
    def setUp(self):
        self.p = p.Pitch()

    def testInit(self):
        with self.subTest("Should have default note value"):
            self.assertEqual(self.p.value, 60)

    def test_as_str(self):
        self.assertEqual(self.p.as_str(), 'C4')

    def testSet(self):
        with self.subTest("Should accept note value"):
            self.p.set(100)
            self.assertEqual(self.p.value, 100)

        with self.subTest("Should accept note name and octave separately"):
            self.p.set('D#', 4)
            self.assertEqual(self.p.value, 63)

        with self.subTest("Should accept full note string"):
            self.p.set('Ab5')
            self.assertEqual(self.p.value, 80)

    def test_transpose_semi(self):
        with self.subTest('It should transpose up'):
            self.p.set(60)
            self.assertEqual(self.p.transpose_semi(2).value, 62)

        with self.subTest("It should transpose down"):
            self.p.set(60)
            self.assertEqual(self.p.transpose_semi(-2).value, 58)

        with self.subTest("It should limit at upper midi bounds"):
            self.p.set(120)
            self.assertEqual(self.p.transpose(10).value, p.MIDI_MAX)

        with self.subTest("It should limit at lower midi bounds"):
            self.p.set(10)
            self.assertEqual(self.p.transpose(-12).value, p.MIDI_MIN)

        with self.subTest("It should wrap up if specified"):
            self.p.set(120)
            self.assertEqual(self.p.transpose(10, 12).value, 118)

        with self.subTest("It should wrap down if specified"):
            self.p.set(10)
            self.assertEqual(self.p.transpose(-14, 12).value, 8)

    def test_transpose_octave(self):
        with self.subTest('It should transpose up'):
            self.p.set(60)
            self.assertEqual(self.p.transpose_octave(2).value, 84)

        with self.subTest("It should transpose down"):
            self.p.set(60)
            self.assertEqual(self.p.transpose_octave(-2).value, 36)

        with self.subTest("It should limit at upper midi bounds"):
            self.p.set(100)
            self.assertEqual(self.p.transpose_octave(3).value, p.MIDI_MAX)

        with self.subTest("It should limit at lower midi bounds"):
            self.p.set(24)
            self.assertEqual(self.p.transpose_octave(-3).value, p.MIDI_MIN)

        with self.subTest("It should wrap up if specified"):
            self.p.set(120)
            self.assertEqual(self.p.transpose_octave(1, 14).value, 118)

        with self.subTest("It should wrap down if specified"):
            self.p.set(10)
            self.assertEqual(self.p.transpose_octave(-1, 10).value, 8)

    def test_magic(self):
        self.p.set(60)

        with self.subTest('call should return value'):
            self.assertEqual(self.p(), 60)

        with self.subTest('print should show note name'):
            self.assertEqual(self.p.__str__(), 'C4')

        with self.subTest('+ should return increased pitch'):
            p2 = self.p + 3
            self.assertEqual(p2.value, 63)

        with self.subTest('- should return decreased pitch'):
            p2 = self.p - 3
            self.assertEqual(p2.value, 57)

        with self.subTest('* should return increased octave'):
            p2 = self.p * 1
            self.assertEqual(p2.value, 72)

        with self.subTest('/ should return decreased octave'):
            p2 = self.p / 1
            self.assertEqual(p2.value, 48)

        with self.subTest('+= should increase pitch'):
            self.p.set(60)
            self.p += 3
            self.assertEqual(self.p(), 63)

        with self.subTest('-= should decrease pitch'):
            self.p.set(60)
            self.p -= 3
            self.assertEqual(self.p(), 57)

        with self.subTest('*= should increase octave'):
            self.p.set(60)
            self.p *= 1
            self.assertEqual(self.p(), 72)

        with self.subTest('/= should decrease octave'):
            self.p.set(60)
            self.p /= 1
            self.assertEqual(self.p(), 48)

if __name__ == '__main__':
    unittest.main()
