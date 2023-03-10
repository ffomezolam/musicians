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

DEFAULT_DURATION = '4n'

# Helper functions

def validate_dur(dstr: str|int):
    "Validate duration string"

    m = RE_DURATION.match(str(dstr))

    if not m: raise ValueError(f'Invalid duration: {dstr}')

    dur, mods = m[1], m[2] or 'n'

    return dur + mods

def split_dur(dstr: str|int):
    "Split duration string into (dur, mods)"

    dstr = validate_dur(dstr)
    m = RE_DURATION.match(dstr)

    return m[1], m[2]

def dur_to_frac(d):
    "Convert duration string to fraction"

    dur, mods = split_dur(d)
    d = Fraction(1, int(dur))
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

    r = d / v

    return frac_to_dur(r)

# Duration class

class Duration:
    "Represents a quantized musical note duration"

    def __init__(self, dur: Optional[int|str|Duration|Fraction] = None):
        self.duration = None

        self.set(dur)

    # Object creation

    def set(self, dur: Optional[int|str|Duration|Fraction] = None):
        "Set duration attributes"

        if type(dur) == Fraction: dur = frac_to_dur(dur)

        self.duration = validate_dur(str(dur)) if dur else DEFAULT_DURATION

        return self

    # Math

    def __eq__(self, dur: int|str|Duration|Fraction):
        "Equality"

        match dur:
            case int() | str():
                return self.duration == validate_dur(dur)
            case Duration():
                return self.duration == dur.duration
            case Fraction():
                return self.duration == frac_to_dur(dur)

        return False

    def __add__(self, other: int|str|Duration|Fraction):
        "Addition"

        v1 = self.as_str()
        other = Duration(other).as_str()
        r = add_durs(v1, other)

        return tuple([Duration(d) for d in r]) if type(r) == tuple else Duration(r)

    def __iadd__(self, other: int|str|Duration|Fraction):
        "In-place addition"

        other = Duration(other)

        self.set(self + other)

        return self

    def __sub__(self, other: int|str|Duration|Fraction):
        "Subtraction"

        v1 = self.as_str()
        other = Duration(other).as_str()
        r = sub_durs(v1, other)

        return tuple([Duration(d) for d in r]) if type(r) == tuple else Duration(r)

    def __isub__(self, other: int|str|Duration|Fraction):
        "In-place subtraction"

        other = Duration(other)

        self.set(self - other)

        return self

    def __mul__(self, multiplier: int|float):
        "Multiplication"

        v1 = self.as_str()
        r = mul_dur(v1, multiplier)

        return tuple([Duration(d) for d in r]) if type(r) == tuple else Duration(r)

    def __imul__(self, multiplier: int|float):
        "In-place multiplication"

        self.set(mul_dur(self.duration, multiplier))

        return self

    def __truediv__(self, divisor: int|float):
        "Division"

        v1 = self.as_str()
        r = div_dur(v1, divisor)

        return tuple([Duration(d) for d in r]) if type(r) == tuple else Duration(r)

    def __idiv__(self, divisor: int|float):
        "In-place division"

        self.set(div_dur(self.duration, divisor))

        return self

    def __round__(self):
        "Rounding strips modifiers"

        return self.__floor__()

    def __floor__(self):
        "Floor operation strips modifiers"

        return Duration(split_dur(self.duration)[0])

    def __ceil__(self):
        "Ceil operation rounds to longer note"

        dur, mods = split_dur(self.duration)

        if mods == 'n': return self.copy()

        if 'd' in mods: return Duration(mul_dur(dur, 2))

        return self.copy()

    # Conversion

    def to_fraction(self):
        "Return duration as a Fraction instance"

        return dur_to_frac(self.duration)

    # String representation

    def as_str(self):
        "Pretty string representation"

        return self.duration

    def __repr__(self):
        return f'{self.__class__}({self.duration})'

    def __str__(self):
        return self.as_str()
