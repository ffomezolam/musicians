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

# Regex

RE_PITCH = re.compile(r'([a-gA-G])(#|b)?\s*(-[1-2]|[0-9])')

# Note values

C = 0
Cs = 1
Db = 1
D = 2
Ds = 3
Eb = 3
E = 4
F = 5
Fs = 6
Gb = 6
G = 7
Gs = 8
Ab = 8
A = 9
As = 10
Bb = 10
B = 11

# Helper functions

def normalize_accidental(accidental: str):
    pass

def parse_pitch(p: str):
    "Return note, octave"

    r = RE_PITCH.match(p)

    if not r: return None

    note, accidental, octave = r[1], ('' if not r[2] else ('s' if r[2] == '#' else 'b')), r[3]

    return note + accidental, octave

def pitch_to_value(note: str, octave: Optional[int] = DEFAULT_OCTAVE):
    "Convert note name (e.g. 'C4') to midi pitch value (0-255)"

    if len(note) > 1:
        r = parse_pitch(note) # get note and octave

        if not r: raise ValueError(f'Invalid note: {note}')

        note, octave = r[1], r[2]

def value_to_pitch(pval: int):
    pass

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

        OptsMixin.__init__(self, DEFAULT_PITCH_OPTS)
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
            pass

        # otherwise we should have an int so it is absolute

    def __repr__(self):
        pass

    def __str__(self):
        pass
