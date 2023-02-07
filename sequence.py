""" sequence.py
---------------
All things Sequencing
"""

from __future__ import annotations
from typing import Optional

import itertools as its
import math
from collections import deque

# Global defaults

DEFAULT_STEPS = 16
DEFAULT_SHIFT = 0
DEFAULT_HITS = 4
DEFAULT_OPTS = {
    "shift-style": "relative", # "relative", "absolute"
    "stretch-with": 0, # int fills with value, "repeat" each hit, "interpolate"
    "expand-with": 0, # int fills with value, "repeat" last value, "loop" sequence
    "replace-style": "expand", # "trim" trims input to length, "expand" expands to fit all
    "interpolate-style": "loop", # "repeat" last value, "loop" to first value
    "interpolate-rounding": "none", # "none", "auto", "up", "down"
    "global-rounding": "auto", # "auto", "up", "down"
}

# Helper functions

def mod(a, b):
    """
    Helper function for correct modulo operations on negative numbers.
    From https://stackoverflow.com/questions/3883004/how-does-the-modulo-operator-work-on-negative-numbers-in-python
    """
    r = a % b
    return r - b if a < 0 else r

def rounder(n, style: str = "auto"):
    match style:
        case "auto":
            return int(n + 0.5)
        case "up":
            return math.ceil(n)
        case "down":
            return math.floor(n)
        case _:
            return n

def list_shift(l: list, amt: int = 0):
    """Helper function for shifting a standard python list"""
    if not amt: return l

    amt = -mod(amt, len(l)) # allow for amounts above length

    return l[amt:] + l[:amt]

def interpolate(val1, val2, num: Optional[int] = 1, func = "linear", rounding_style: str = "none"):
    """Interpolate num values between val1 and val2"""

    if val1 == val2: return [val1 for _ in range(num)]

    mult = (val2 - val1) / (num + 1)

    return [rounder(val1 + (mult * i), rounding_style) for i in range(1, num + 1)]

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

        style = style or self.getopts('replace-style')

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

        style = style or self.getopts('shift-style')

        if style == 'absolute':
            amount -= self.offset
            self.seq = list_shift(self.seq, amount)
            self.offset = amount
        else:
            self.seq = list_shift(self.seq, amount)
            self.offset += amount

        return self

    def stretch_to(self, size: Optional[int] = None, style: Optional[int|str] = -1,
        *,
        interpolate_style: Optional[str] = None,
        interpolate_rounding: Optional[str] = None
    ):
        """
        Stretch sequence to size, creating/removing intermediate values.
        Stretching to larger irregular sizes will try to spread values as
        evenly as possible, e.g. [1,2,3,4] stretched to size 6 should look
        like [1,0,2,3,0,4] and to size 7: [1,0,2,0,3,0,4]
        """

        if not size: return self

        style = self.getopts('stretch-with') if style is None or (type(style) == int and style < 0) else style
        interpolate_style = interpolate_style or self.getopts('interpolate-style')
        interpolate_rounding = interpolate_rounding or self.getopts('interpolate-rounding')

        if size > self.steps:
            # get divisible and remainder
            num, extra = divmod(size, self.steps)
            num -= 1 # adjust for existing step entries

            result = [[self.seq[i]] for i in range(self.steps)]

            # only automate adding markers if size is more than twice step count
            if size >= self.steps * 2:
                for i in range(self.steps): result[i] += [-1 for _ in range(num)]

            # convert result to a model with -1 as values to fill
            if extra:
                # we have a remainder, need to distribute by euclidean model
                model = generate_euclidean(len(result) + extra, len(result))

                # all zeros in model are the distributed items
                result = list(its.chain.from_iterable([result.pop(0) if hit else [-1] for hit in model]))
            else:
                result = list(its.chain.from_iterable(result))

            # Replace -1 entries
            match style:
                case int():
                    # integer replacement
                    result = [style if i < 0 else i for i in result]
                case "repeat":
                    # repeat last value
                    for ix in range(len(result)):
                        if result[ix] < 0:
                            result[ix] = result[ix - 1]
                case "interpolate":
                    q = []

                    # get bounding indices of interpolatable values
                    for ix, val in enumerate(result):
                        # add index to queue
                        if val >= 0:
                            q.append(ix)

                        # handle 2 indices
                        if len(q) >= 2:
                            # get indices and reset q
                            ix1, ix2, q = q[0], q[1], [] # get ixs and reset q

                            # check for space beween indices
                            if ix2 - ix1 > 1:
                                # we have 2 indices with space between so can interpolate
                                n = ix2 - ix1 - 1 # number of entries between indices

                                # get interpolated values
                                ivals = interpolate(result[ix1], result[ix2], n, interpolate_rounding)

                                # sub values into sequence
                                for vix, six in enumerate(range(ix1 + 1, ix2)):
                                    result[six] = ivals[vix]

                            q.append(ix2) # start again at second index

                    # handle last elements (if necessary)
                    if result[-1] < 0:
                        last_ix = q[0] # index of last non-distributed element
                        val = result[last_ix] # last value

                        # set final distributed elements based on style
                        match interpolate_style:
                            case 'loop':
                                # loop interpolation to first value
                                n = len(result) - last_ix - 1 # number of entries

                                # get interpolated values
                                ivals = interpolate(val, result[0], n, interpolate_rounding)

                                # replace with interpolated values
                                for vix, six in enumerate(range(last_ix + 1, len(result))):
                                    result[six] = ivals[vix]

                            case 'repeat':
                                # repeat last value
                                for i in range(last_ix + 1, len(result)):
                                    result[i] = val

            # cache and replace sequence
            if not self._cache: self._cache = self.seq
            self.set(result)

        elif size < self.steps:
            # get model to distribute items
            model = generate_euclidean(self.steps, size)

            # ones in model are remaining items
            result = [self.seq[i] for i in range(self.steps) if model[i]]

            # cache and replace sequence
            if not self._cache: self._cache = self.seq
            self.set(result)

        return self

    def stretch_by(self, mult: Optional[float] = 2, style: Optional[int|str] = -1,
        *,
        interpolate_style: Optional[str] = None,
        interpolate_rounding: Optional[str] = None,
        mult_rounding: Optional[str] = None
    ):
        """Stretch sequence by multiplier, creating/removing intermediate values"""
        roundmethod = mult_rounding or self.getopts('global-rounding')
        size = rounder(self.steps * mult, roundmethod)

        return self.stretch_to(size, style,
                               interpolate_style = interpolate_style,
                               interpolate_rounding = interpolate_rounding)

    def shrink_to(self, *args, **kwargs):
        """Alias for stretch_to()"""

        return self.stretch_to(*args, **kwargs)

    def shrink_by(self, div, *args, **kwargs):
        """Reverse of stretch_by() (as in will divide instead of multiply)"""

        mult = 1 / div

        return self.stretch_by(mult, *args, **kwargs)

    def expand_to(self, size: Optional[int], style: Optional[str] = None):
        """Expand sequence to size, adding/removing values at end"""
        pass

    def expand_by(self, size: Optional[int] = 2, style: Optional[str] = None):
        """Expand sequence by multiplier, adding/removing values at end"""
        pass

    def contract_to(self):
        """Alias for expand_to()"""
        pass

    def contract_by(self):
        """Reverse of expand_by() (as in will divide instead of multiply)"""
        pass

    def reset(self):
        """Reset to original sequence (i.e. undo all)"""
        if self._cache:
            self.set(self._cache)
            self._cache = None

        return self

    ## Step/value manipulation

    def replace_value(self, value, rvalue, limit: int = 0):
        """Replace specified value in sequence with another value"""
        pass

    def replace_step(self, step, value):
        """Replace value at step with specified value"""
        pass

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
