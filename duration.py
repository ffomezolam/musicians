""" duration.py
---------------
Functions and classes for working with quantized musical note durations.

This uses note values similar to those used in Max/MSP, e.g. 4n, 4d.
"""

from __future__ import annotations
from typing import Optional

import re

from fractions import Fraction

import itertools as its

# durations: 64, 32, 16, 8, 4, 2, 1
# modifiers: [d]otted, [t]riplet

# Constants

RE_DURATION = re.compile(r'(64|32|16|8|4|2|1)(d?t?|n?)')

DURATIONS = {1, 2, 4, 8, 16, 32, 64}

MODIFIERS = {'d', 't'}

MOD_DURATIONS = {
    '1n': Fraction(1, 1),
    '2d': Fraction(1, 2) + Fraction(1, 4),
    '2n': Fraction(1, 2),
    '4d': Fraction(1, 4) + Fraction(1, 8),
    '4n': Fraction(1, 4),
    '8d': Fraction(1, 8) + Fraction(1, 16),
    '8n': Fraction(1, 8),
    '16d': Fraction(1, 16) + Fraction(1, 32),
    '16n': Fraction(1, 16),
    '32d': Fraction(1, 32) + Fraction(1, 64),
    '32n': Fraction(1, 32),
    '64n': Fraction(1, 64),
    Fraction(1, 1): '1n',
    Fraction(1, 2) + Fraction(1, 4): '2d',
    Fraction(1, 2): '2n',
    Fraction(1, 4) + Fraction(1, 8): '4d',
    Fraction(1, 4): '4n',
    Fraction(1, 8) + Fraction(1, 16): '8d',
    Fraction(1, 8): '8n',
    Fraction(1, 16) + Fraction(1, 32): '16d',
    Fraction(1, 16): '16n',
    Fraction(1, 32) + Fraction(1, 64): '32d',
    Fraction(1, 32): '32n',
    Fraction(1, 64): '64n',
}

DUR_STRINGS = [k for k in MOD_DURATIONS if type(k) == str]
DUR_FRACTIONS = [k for k in MOD_DURATIONS if type(k) == Fraction]

DEFAULT_DURATION = 4

# Helper functions

def parse_dur_str(dstr: str|int):
    "Parse duration string"

    if type(dstr) == int: dstr = str(int)

    m = RE_DURATION.match(dstr)

    if not m: raise ValueError(f'Invalid duration: {dstr}')

    return int(m[1]), m[2]

def parse_mods(mods: str|tuple|list|set):
    "Verify and format modifiers"
    match mods:
        case str():
            mods = [c for c in mods]
        case tuple() | list() | set():
            mods = list(mods)
        case _:
            mods = []

    mods = [mod for mod in mods if mod in MODIFIERS]

    return set(mods)

def dur_to_frac(d):
    "Convert duration string to fraction"

    ds = parse_dur_str(d)
    mods = parse_mods(ds[1])
    d = Fraction(1, ds[0])
    if 'd' in mods: d += (d / 2)

    return d

def frac_to_dur(f: int|float|Fraction):
    "Convert fraction to a duration"

    if type(f) != Fraction: f = Fraction(f)

    if f in MOD_DURATIONS: return MOD_DURATIONS[f]

    # get simplest set of notes that add to f
    def _frac_to_dur(f, _):
        if f in MOD_DURATIONS:
            _.append(MOD_DURATIONS[f])
        else:
            for df in DUR_FRACTIONS:
                if df < f and df.numerator == 1:
                    _.append(MOD_DURATIONS[df])
                    _frac_to_dur(f - df, _)
                    break

        return _

    return tuple(_frac_to_dur(f, []))

def add_durs(d1, d2):
    "Add durations"

    dr = [dur_to_frac(d1), dur_to_frac(d2)]

    r = dr[0] + dr[1]

    return frac_to_dur(r)

def sub_durs(d1, d2):
    "Subtract durations"

    dr = [dur_to_frac(d1), dur_to_frac(d2)]

    r = dr[0] - dr[1]

    return frac_to_dur(r)

def mul_dur(d, m):
    "Multiply duration"

    d = dur_to_frac(d)

    r = d * m

    return frac_to_dur(r)

def div_dur(d, v):
    "Divide duration"

    d = dur_to_frac(d)

    r = d / m

    return frac_to_dur(r)

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
                return self.duration == dur and self.modifiers == mods
            case Duration():
                return self.duration == other.duration and self.modifiers == other.modifiers

        return False

    def __add__(self, other: int|str|Duration):
        "Addition"

        v1 = self.as_str()
        other = Duration(other).as_str()
        r = add_durs(v1, other)

        return tuple([Duration(d) for d in r]) if type(r) == tuple else Duration(r)

    def __sub__(self, other: int|str|Duration):
        "Subtraction"

        v1 = self.as_str()
        other = Duration(other).as_str()
        r = sub_durs(v1, other)

        return tuple([Duration(d) for d in r]) if type(r) == tuple else Duration(r)

    def __mul__(self, multiplier: int|float):
        "Multiplication"

        v1 = self.as_str()
        r = mul_dur(v1, multiplier)

        return tuple([Duration(d) for d in r]) if type(r) == tuple else Duration(r)

    def __truediv__(self, divisor: int|float):
        "Division"

        v1 = self.as_str()
        r = div_dur(v1, divisor)

        return tuple([Duration(d) for d in r]) if type(r) == tuple else Duration(r)

    # String representation

    def as_str(self):
        "Pretty string representation"

        # enforce 'd' before 't'
        modifiers = self.modifiers
        if modifiers == set('dt'): modifiers = 'dt'
        elif not modifiers: modifiers = 'n'

        return f'{self.duration}{"".join(modifiers)}'

    def __repr__(self):
        return f'{self.__class__}({self.duration, self.modifiers})'

    def __str__(self):
        return self.as_str()
