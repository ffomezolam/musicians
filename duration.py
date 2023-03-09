""" duration.py
---------------
Functions and classes for working with quantized musical note durations.
"""

from __future__ import annotations
from typing import Optional

import re

from fraction import Fraction

# durations: 64, 32, 16, 8, 4, 2, 1
# modifiers: [d]otted, [t]riplet

# Constants

RE_DURATION = re.compile(r'(64|32|16|8|4|2|1)(d?t?)')

DURATIONS = {1, 2, 4, 8, 16, 32, 64}

MODIFIERS = {'d', 't'}

DEFAULT_DURATION = 4

# Helper functions

def parse_dur_str(dstr: str):
    "Parse duration string"
    m = RE_DURATION.match(dstr)

    if not m: raise ValueError(f'Invalid duration: {dstr}')

    print(f'DURSTR: {m.groups()}, {m[1]}, {m[2]}')

    return int(m[1]), m[2]

def parse_mods(mods: str|tuple|list|set):
    "Verify and format modifiers"
    print(f'MODS: {mods}')

    match mods:
        case str():
            mods = [c for c in mods]
        case tuple() | list() | set():
            mods = list(mods)
        case _:
            mods = []

    mods = [mod for mod in mods if mod in MODIFIERS]

    return set(mods)

def add_durs(d1, d2):
    pass

def sub_durs(d1, d2):
    pass

def mul_dur(d, m):
    pass

def div_dur(d, v):
    pass

# Duration class

class Duration:
    "Represents a quantized musical note duration"

    def __init__(self,
                 dur: Optional[int|str|Duration] = None,
                 mods: Optional[str|tuple|list|set] = None
    ):
        self.duration = None
        self.modifiers = None

        self.set(dur, mods)

    # Object creation

    def set(self,
            dur: Optional[int|str|Duration] = None,
            mods: Optional[str|tuple|list|set] = None
    ):
        "Set duration attributes"

        match dur:
            case int():
                if dur in DURATIONS:
                    self.duration = dur
                    self.modifiers = parse_mods(mods)

            case str():
                duration, modifiers = parse_dur_str(dur)

                self.duration = duration
                self.modifiers = parse_mods(modifiers or mods)

            case Duration():
                self.duration = dur.duration
                self.modifiers = dur.modifiers

            case _:
                self.duration = DEFAULT_DURATION
                self.modifiers = set()

        return self

    # Math

    def __eq__(self, other: int|str|Duration):
        "Equality"
        match other:
            case int():
                return self.duration == other
            case str():
                dur, mods = parse_dur_str(other)
                mods = parse_mods(mods)
                return self.duration == dur and self.modifiers = mods
            case Duration():
                return self.duration == other.duration and self.modifiers == other.modifiers

        return False

    def __add__(self, other: int|str|Duration):
        "Addition"
        pass

    def __sub__(self, other: int|str|Duration):
        "Subtraction"
        pass

    def __mul__(self, other: int|float):
        "Multiplication"
        pass

    def __truediv__(self, other: int|float):
        "Division"
        pass

    # String representation

    def as_str(self):
        "Pretty string representation"

        # enforce 'd' before 't'
        modifiers = self.modifiers
        if modifiers == set('dt'): modifiers = 'dt'

        return f'{self.duration}{"".join(modifiers)}'

    def __repr__(self):
        return f'{self.__class__}({self.duration, self.modifiers})'

    def __str__(self):
        return self.as_str()
