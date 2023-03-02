""" Pitch.py
-----------
Class representing a musical pitch and helper functions for working with pitch
data
"""

from __future__ import annotations
from typing import Optional
import re
from enum import Enum

# Instance option methods

from opts import OptsMixin

# Defaults

from pitch_defaults import MIDDLE_C_OCTAVE, DEFAULT_NOTE, DEFAULT_OCTAVE

# Pitch names

NOTE = {
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
    "B": 11
}

OFFSET = [
    "C",
    ("Cs", "Db"),
    "D",
    ("Ds", "Eb"),
    "E",
    "F",
    ("Fs", "Gb"),
    "G",
    ("Gs", "Ab"),
    "A",
    ("As", "Bb"),
    "B"
]

# Regex

RE_PITCH = re.compile(r'([a-gA-G])(#|b)?\s*(-[1-2]|[0-9])?')
RE_ACCIDENTAL = re.compile(r'[#sb]')

# Helper functions

def offset_to_note(offset: int):
    pass

def note_to_offset(note: str|int):
    pass

def _normalize_accidental(pstr: str):
    "Format accidental for use with offset collections"
    pass

def parse_pitch_str(p: str):
    "Return pitch, accidental, octave"

    r = RE_PITCH.match(p)

    if not r: raise ValueError(f'Invalid pitch: {p}')

    pstr, accidental, octave = r[1] or DEFAULT_NOTE, r[2] or '', r[3] or DEFAULT_OCTAVE

    return pstr, accidental, int(octave)

def pitch_to_value(pstr: str, octave: Optional[int] = DEFAULT_OCTAVE,
                   *,
                   middle_c_octave: int = MIDDLE_C_OCTAVE
    ):
    "Convert pitch name (e.g. 'C4') to midi pitch value (0-255)"

    if type(pstr) == int: return pstr

    if len(pstr) > 1:
        pstr, octave = parse_pitch(pstr) # get pstr and octave

    return 60 + (12 * (octave - middle_c_octave)) + OFFSETS[pstr]

def ptv(*args, **kwargs):
    "Alias for pitch_to_value()"
    return pitch_to_value(*args, **kwargs)

def value_to_pitch(pval: int,
                   *,
                   middle_c_octave: int = MIDDLE_C_OCTAVE
    ):
    "Convert pitch value to pitch name"

    aboct, poff = divmod(pval, 12) # get absolute octave and pitch offset

    octave = int(middle_c_octave + (((aboct * 12) - 60) / 12))

    return

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
        self.note = None
        self.octave = None

        OptsMixin.__init__(self, DEFAULT_NOTE_OPTS)
        self.setopts(options)

        self.set(note, octave)

    def set(self, note: str|int = DEFAULT_NOTE, octave: int = DEFAULT_OCTAVE):
        """
        Set pitch value by note and octave.
        Can pass int to `note` argument to directly set pitch value.
        Can pass string and int (e.g. 'C4') to set by note and octave.
        """

        if type(note) == str:
            # convert note/octave to absolute value

            if RE_PITCH.match(note):
                # separate note string (i.e. 'C4')
                note, octave = parse_pitch(note)

        # otherwise we should have an int so it is absolute

    def __repr__(self):
        pass

    def __str__(self):
        pass
