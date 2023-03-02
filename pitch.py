""" Pitch.py
-----------
Class representing a musical pitch and helper functions for working with pitch
data
"""

from __future__ import annotations
from typing import Optional
import re

# Instance option methods

from opts import OptsMixin

# Defaults

from pitch_defaults import MIDDLE_C_OCTAVE, DEFAULT_NOTE, DEFAULT_OCTAVE, DEFAULT_LEAN

# Pitch offsets

OFFSET = {
    "C": 0,
    "Cs": 1,
    "Db": 1,
    "D": 2,
    "Ds": 3,
    "Eb": 3,
    "E": 4,
    "F": 5,
    "Fs": 6,
    "Gb": 6,
    "G": 7,
    "Gs": 8,
    "Ab": 8,
    "A": 9,
    "As": 10,
    "Bb": 10,
    "B": 11,
    0: "C",
    1: ("Cs", "Db"),
    2: "D",
    3: ("Ds", "Eb"),
    4: "E",
    5: "F",
    6: ("Fs", "Gb"),
    7: "G",
    8: ("Gs", "Ab"),
    9: "A",
    10: ("As", "Bb"),
    11: "B"
}

# Regex

RE_NOTE = re.compile(r'([a-gA-G])([#sb]*)', re.A)
RE_ACCIDENTAL = re.compile(r'()([#sb])()', re.A)
RE_PITCH = re.compile(r'^\s*([a-gA-G])([#sb]*)\s*(-?\d{1,2})?\s*$', re.A)

# Helper functions

def format_accidental(note: str, style: str = 'letter'):
    "Format accidental for symbol or letter styles"

    n = a = o = ''

    # match pitch or accidental
    for m in [RE_PITCH.match(note), RE_ACCIDENTAL.search(note), re.match('()()()', '')]:
        if m:
            n, a, o = m.groups()

            if not o: o = ''

            if style == 'letter' and a == '#': a = 's'
            elif style == 'symbol' and a == 's': a = '#'

            break

    return n + a + o

def _lean_to_tuple(lean: int):
    "Adjust lean value to tuple-friendly value"

    if not lean: lean = 1

    if lean > 0: lean= 0
    else: lean = 1

    return lean

def _offset(o: str|int, lean: int = 1):
    "Get value from offset table"

    if type(o) == str:
        return OFFSET[o]
    else:
        lean = _lean_to_tuple(lean)

        o = o % 12

        match OFFSET[o]:
            case str():
                return OFFSET[o]
            case tuple():
                return OFFSET[o][lean]

def _midirange(val: int):
    "Limit value to midi range"
    if val < 0: val = 0
    elif val > 127: val = 127

    return val

def offset_to_note(offset: int, lean: int = DEFAULT_LEAN):
    "Convert offset to note"

    return _offset(offset, lean)

def note_to_offset(note: str):
    "Convert note to offset"

    return _offset(note)

def parse_pitch(p: str|int):
    "Return pitch, accidental, octave"

    if type(p) == int: return p

    r = RE_PITCH.match(p)

    if not r: raise ValueError(f'Invalid pitch: {p}')

    pstr, accidental, octave = r[1] or DEFAULT_NOTE, r[2] or '', r[3] or DEFAULT_OCTAVE

    return pstr, _normalize_accidental(accidental), int(octave)

def pitch_to_value(pstr: str, octave: Optional[int] = DEFAULT_OCTAVE,
                   *,
                   middle_c_octave: int = MIDDLE_C_OCTAVE
    ):
    "Convert pitch name (e.g. 'C4') to midi pitch value (0-255)"

    if type(pstr) == int: return pstr

    if len(pstr) > 1:
        n, a, octave = parse_pitch(pstr) # get note, accidental, octave
        pstr = n + a

    return 60 + (12 * (octave - middle_c_octave)) + OFFSET[pstr]

def ptv(*args, **kwargs):
    "Alias for pitch_to_value()"
    return pitch_to_value(*args, **kwargs)

def value_to_pitch(pval: int, lean: int = DEFAULT_LEAN,
                   *,
                   middle_c_octave: int = MIDDLE_C_OCTAVE
    ):
    "Convert pitch value to pitch name"

    # convert lean to tuple-friendly value
    lean = _lean_to_tuple(lean)

    aboct, poff = divmod(pval, 12) # get absolute octave and pitch offset

    octave = int(middle_c_octave + (((aboct * 12) - 60) / 12))

    return _offset(poff, lean) + str(octave)

def vtp(*args, **kwargs):
    "Alias for value_to_pitch()"
    return value_to_pitch(*args, **kwargs)

# Pitch class

class Pitch(OptsMixin):
    """
    Represents a musical pitch
    """

    def __init__(self,
                 note: Optional[str|int] = None,
                 octave: Optional[int] = None,
                 *,
                 options: Optional[dict] = None
    ):
        self.value = None

        OptsMixin.__init__(self)
        self.setopts(options)

        self.set(note, octave)

    def set(self,
            note: Optional[str|int] = None,
            octave: Optional[int] = None
    ):
        """
        Set pitch value by note and octave.
        Can pass int to `note` argument to directly set pitch value.
        Can pass string and int (e.g. 'C4') to set by note and octave.
        """

        if note is None: note = DEFAULT_NOTE
        if octave is None: octave = DEFAULT_OCTAVE

        if type(note) == int:
            note = _midirange(note)
            self.value = note
        else:
            n, a, o = parse_pitch(DEFAULT_NOTE)

            if octave: o = octave

            self.value = pitch_to_value(n + a + str(o))

        return self

    # Printing

    def as_str(self):
        "Return a nice looking human-readable string"
        return format_accidental(value_to_pitch(self.value), 'symbol')

    def __repr__(self):
        return f'Pitch({self.value})'

    def __str__(self):
        return f'{self.as_str()}'
