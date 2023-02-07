""" sequence.py
---------------
All things Sequencing
"""

from __future__ import annotations
from typing import Optional

import itertools as its
import math

# Global defaults

DEFAULT_STEPS = 16
DEFAULT_SHIFT = 0
DEFAULT_HITS = 4
DEFAULT_OPTS = {
    "shift-style": "relative", # "relative", "absolute"
    "stretch-with": 0, # int fills with value, "repeat" each hit, "interpolate"
    "expand-with": 0, # int fills with value, "repeat" last value, "loop" sequence
    "replace-style": "expand", # "trim" trims input to length, "expand" expands to fit all
}

# Helper functions

def mod(a, b):
    """
    Helper function for correct modulo operations on negative numbers.
    From https://stackoverflow.com/questions/3883004/how-does-the-modulo-operator-work-on-negative-numbers-in-python
    """
    r = a % b
    return r - b if a < 0 else r

def list_shift(l: list, amt: int = 0):
    """Helper function for shifting a standard python list"""
    if not amt: return l

    amt = -mod(amt, len(l)) # allow for amounts above length

    return l[amt:] + l[:amt]

def split(l, rounding = "up"):
    """Generate a list from first and len / 2 values, recursively"""

    result = []
    round_up = False if "down" in rounding else True

def distribute(vals, l, rounding = "up"):
    """Distribute values list (vals) across list (l) as evenly as possible"""

    pass

def interpolate(val1, val2, num: Optional[int] = 1, func = "linear"):
    """Interpolate num values between val1 and val2"""

    if val1 == val2: return [val1 for _ in range(num)]

    mult = (val2 - val1) / (num + 1)

    return [val1 + (mult * i) for i in range(1, num + 1)]

# Generator functions

def generate_euclidean(steps: int = DEFAULT_STEPS, hits: int = DEFAULT_HITS, shift: int = DEFAULT_SHIFT) -> list:
    """Generate a euclidean rhythm as a python list"""

    # create list with hits first and rests after
    coll = [[1] if step < hits else [0] for step in range(steps)]
    while hits > 1:
        quotient, remainder = divmod(steps, hits)
        for i in range(quotient - 1):
            for j in range(hits):
                item = coll.pop()
                coll[j] += item
        hits = remainder
        steps = len(coll)

    coll = list(its.chain.from_iterable(coll))
    if shift: coll = list_shift(coll, shift)

    return coll

# Class code

class Sequence():
    """
    Class representing a single musical sequence. For purposes of this class,
    all indices are represented as beats, and therefore counting starts at 1.

    Can pass a list to the constructor to initialize the sequence to the list.

    Can also pass a dict of options to set up how various methods work.

    Public Attributes
    -----------------
    steps: int
        number of steps in sequence
    hits: int
        number of non-0 values in sequence
    offset: int
        shift offset of sequence
    seq: list
        the sequence as a list
    """

    def __init__(self, sequence: Optional[list] = None, options: Optional[dict] = None):
        self.steps = 0
        self.hits = 0
        self.offset = 0

        self.seq = None
        self._cache = None

        self._opts = DEFAULT_OPTS.copy()

        self.setopts(options)
        self.set(sequence)

    # Option handling

    def setopts(self, opts: Optional[dict|str] = DEFAULT_OPTS, val = None):
        """Set instance options"""
        if opts:
            if type(opts) == dict:
                for k, v in opts.items():
                    if k in self._opts: self._opts[k] = v
            elif val:
                k, v = opts, val
                if k in self._opts: self._opts[k] = v

        return self

    def getopts(self, opt: Optional[str] = None):
        """Get instance options"""
        if not opt: return self._opts

        return self._opts.get(opt, None)

    # Sequence creation

    def set(self, sequence: Optional[list|Sequence] = None):
        """Set sequence"""
        if not sequence:
            # set to a blank sequence
            return self.set([0 for _ in range(DEFAULT_STEPS)])
        elif type(sequence) == int:
            # set to a blank sequence with specified steps
            return self.set([0 for _ in range(sequence)])
        elif isinstance(sequence, Sequence):
            # copy sequence contents
            return self.set(sequence.seq)
        else:
            self.seq = sequence
            self.steps = len(self.seq)
            self.hits = sum([1 if item > 0 else 0 for item in self.seq])
            self.offset = 0

        return self

    def copy(self):
        """Create copy of sequence"""
        return Sequence(self.seq, self._opts)

    def insert(self, sequence, beat: int = 1):
        """
        Insert sequence at beat, shifting current sequence.
        Beat 0 is start.
        """
        if isinstance(sequence, Sequence): sequence = sequence.seq

        idx = beat - 1

        self.set(self.seq[:idx] + sequence + self.seq[idx:])

        return self

    def remove(self, *args: int):
        """
        Remove part of sequence
        1 arg: remove length from start/end
        2 args: remove length starting at beat
        """
        start = 1
        length = 4

        if len(args) == 1:
            length = args[0]

            if length < 0:
                start = self.steps + length + 1
                length = -length

        elif len(args) > 1:
            start = args[0]
            length = args[1]

        # convert beats to index
        start -= 1

        end = start + length

        self.set(self.seq[:start] + self.seq[end:])

        return self

    def append(self, sequence):
        """Append sequence to end"""
        if isinstance(sequence, Sequence): sequence = sequence.seq

        self.set(self.seq + sequence)

        return self

    def prepend(self, sequence):
        """Prepend sequence to start"""
        return self.insert(sequence)

    def replace(self, sequence, beat: int = 1, style: Optional[str] = None):
        """Replace portion of sequence"""
        if not style: style = self.getopts('replace-style')

        if len(sequence) > self.steps: self.set(sequence)

        # convert beat to index
        start = beat - 1
        end = start + len(sequence)

        if end < self.steps:
            # can replace within current bounds
            self.set(self.seq[:start] + sequence + self.seq[end:])
        else:
            # replacement length exceeds current bounds
            if style == 'trim':
                newlen = self.steps - start
                self.set(self.seq[:start] + sequence[:newlen])
            else: # style == 'expand'
                self.set(self.seq[:start] + sequence)

        return self

    # Sequence manipulation

    def shift(self, amount: int = DEFAULT_SHIFT, style: Optional[str] = None):
        """Shift sequence"""
        if not style: style = self.getopts('shift-style')

        if style == 'absolute':
            amount -= self.offset
            self.seq = list_shift(self.seq, amount)
            self.offset = amount
        else:
            self.seq = list_shift(self.seq, amount)
            self.offset += amount

        return self

    def stretch_to(self, size: Optional[int], style: Optional[str] = None):
        """
        Stretch sequence to size, creating/removing intermediate values.
        Stretching to larger irregular sizes will try to spread values as
        evenly as possible, e.g. [1,2,3,4] stretched to size 6 should look
        like [1,0,2,3,0,4] and to size 7: [1,0,2,0,3,0,4]
        """

        if not style: style = self.getopts('stretch-with')

        if size > self.steps:
            # get divisible and remainder
            num, extra = divmod(size, self.steps)
            num -= 1 # adjust for existing step entries
            result = []

            # only automate adding markers if size is more than twice step count
            if size >= self.steps * 2:
                for i in range(self.steps): result.append([self.seq[i]] + [-1 for _ in range(num)])

            # we have a remainder, need to distribute by euclidean model
            model = generate_euclidean(len(result) + extra, len(result))

            # all zeros in model are the distributed items
            distributed = its.chain.from_iterable([result.pop(0) if hit else [-1] for i in model])

            # TODO: need to replace -1 entries
            match style:
                case int():
                    # integer replacement
                    distributed = [style if i < 0 else i for i in distributed]
                case "repeat":
                    # repeat last value
                    for ix in range(len(distributed)):
                        if distributed[ix] < 0:
                            distributed[ix] = distributed[ix - 1]
                case "interpolate":
                    pass


            # cache and replace sequence
            if not self._cache: self._cache = self.seq
            self.set(distributed)

        elif size < self.steps:
            # get model to distribute items
            model = generate_euclidean(self.steps, size)

            # ones in model are remaining items
            distributed = its.chain.from_iterable([self.seq[i] for i in self.steps if model[i]])

            # cache and replace sequence
            if not self._cache: self._cache = self.seq
            self.set(distributed)

        return self

    def stretch_by(self, mult: Optional[float] = 2, style: Optional[str] = None):
        """Stretch sequence by multiplier, creating/removing intermediate values"""
        pass

    def expand_to(self, size: Optional[int], style: Optional[str] = None):
        """Expand sequence to size, adding/removing values at end"""
        pass

    def expand_by(self, size: Optional[int] = 2, style: Optional[str] = None):
        """Expand sequence by multiplier, adding/removing values at end"""
        pass

    def reset(self):
        """Reset to original sequence (i.e. undo all)"""
        if self._cache:
            self.set(self._cache)
            self._cache = None

        return self

    # Sequence querying

    def as_list(self):
        """Get sequence as list"""
        return self.seq

    def __call__(self):
        return self.as_list()

    def __len__(self):
        """Sequence length"""
        return self.steps

    def __getitem__(self, beat: int):
        """Get hit by bracket notation"""
        return self.seq[beat - 1]

    def __setitem__(self, beat: int, value: int):
        """Set hit by bracket notation"""
        self.seq[beat - 1] = value

    def __iter__(self):
        """Iterate over hits"""
        return (i for i in self.seq)

    # String representation

    def __repr__(self):
        return f'{self.seq}'

    def __str__(self):
        return f'{self.steps}:{self.hits} {self.seq}'
