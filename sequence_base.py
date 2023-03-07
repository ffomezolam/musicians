""" sequence_base.py
--------------------
Contains abstract base class for sequences an helpful sequence functions
"""

from __future__ import annotations
from typing import Optional

from abc import ABC, abstractmethod # abstract base class support
from collections.abc import MutableSequence

import itertools as its

# Defaults

from sequence_defaults import DEFAULT_STEPS, DEFAULT_HITS, DEFAULT_SHIFT

# Helpers

from helpers import mod, rounder, interpolate

# Sequence manipulation functions

def shift_seq(l: list, amt: int = 0):
    """Helper function for shifting a standard python list"""
    if not amt: return l

    amt = -mod(amt, len(l)) # allow for amounts above length

    return l[amt:] + l[:amt]

def stretch_seq(seq: list,
                size: int,
                style: Optional[int|str] = "repeat",
                istyle: Optional[str] = "loop",
                iround: Optional[str] = "none"
):
    """
    Function for stretching (or shrinking) a list.

    Parameters
    ----------
    seq
        The list to stretch
    size
        The size to stretch to
    style
        Stretch style. Valid values: int, "repeat", "interpolate"
    istyle
        Interpolate style. Valid values: "loop", "repeat"
    iround
        Rounding style. Valide values: "none", "auto", "up", "down"
    """

    if not size or not seq: return []

    if type(style) != int and style not in ("repeat", "interpolate"): style = "repeat"
    if istyle not in ("loop", "repeat"): istyle = "loop"
    if iround not in ("auto","none","up","down"): iround = "none"

    steps = len(seq)

    if size > steps:
        # get divisible and remainder
        num, extra = divmod(size, steps)
        num -= 1 # adjust for existing steps

        result = [[seq[i]] for i in range(steps)]

        if size >= steps * 2:
            # size more than twice step count so we can quickly insert model markers
            for i in range(steps): result[i] += [-1 for _ in range(num)]

        if extra:
            # there is a remainder so distribute by euclidean model
            model = generate_euclidean(len(result) + extra, len(result))

            result = list(its.chain.from_iterable([result.pop(0) if hit else [-1] for hit in model]))
        else:
            result = list(its.chain.from_iterable(result))

        # fill model
        match style:
            case int():
                # replace with integer
                result = [style if i < 0 else i for i in result]

            case "repeat":
                # repeat last value
                for ix in range(len(result)):
                    if result[ix] < 0:
                        result[ix] = result[ix - 1]

            case "interpolate":
                q = []

                # get bounding indices
                for ix, val in enumerate(result):
                    # add index to queue
                    if val >= 0:
                        q.append(ix)

                    # handle 2 indices
                    if len(q) >= 2:
                        # get indices and reset q
                        ix1, ix2, q = q[0], q[1], []

                        # check for space between indices
                        if ix2 - ix1 > 1:
                            # have space so can interpolate
                            n = ix2 - ix1 - 1 # num entries between indices

                            # get interpolated values
                            ivals = interpolate(result[ix1], result[ix2], n, rounding_style=iround)

                            # sub values into sequence
                            for vix, six in enumerate(range(ix1 + 1, ix2)):
                                result[six] = ivals[vix]

                        q.append(ix2) # restart from second index

                # handle trailing elements if necessary
                if result[-1] < 0:
                    last_ix = q[0] # index of last hit
                    val = result[last_ix] # last value

                    # set trailing elements based on style
                    match istyle:
                        case "loop":
                            # interpolate to first value
                            n = len(result) - last_ix - 1 # number of entries

                            # get interpolated values
                            ivals = interpolate(val, result[0], n, rounding_style=iround)

                            # replace with interpolated values
                            for vix, six in enumerate(range(last_ix + 1, len(result))):
                                result[six] = ivals[vix]

                        case "repeat":
                            # repeat last value
                            for i in range(last_ix + 1, len(result)):
                                result[i] = val

        return result

    elif size < steps:
        # get model to distribute items
        model = generate_euclidean(steps, size)

        # ones in model are remaining items
        result = [seq[i] for i in range(steps) if model[i]]

        return result

def shrink_seq(seq: list, size: int, style: int|str = "repeat", istyle: str = "loop", iround: str = "none"):
    "Alias for stretch_seq()"
    return stretch_seq(seq, size, style, istyle, iround)

def expand_seq(seq: list, size: int, style: int|str = 0, looplen = 0, iround = "none"):
    "Expand sequence by adding elements at end"
    if type(style) != int and style not in ("repeat", "loop", "interpolate"): style = 0

    steps = len(seq)

    seq = seq.copy()

    if size > steps:
        match style:
            case int():
                # fill with int
                n = style
                for _ in range(size - steps):
                    seq.append(n)

            case "repeat":
                # fill with last value
                n = seq[-1]
                for _ in range(size - steps):
                    seq.append(n)

            case "loop":
                # adjust loop length for a 0 value
                if not looplen: looplen = steps

                # create loop
                loop = seq[-looplen:]

                # append loop to new end
                for i in range(size - steps):
                    seq.append(loop[i % len(loop)])

            case "interpolate":
                # get interpolated values
                start = seq[-1]
                end = seq[0]
                n = size - steps

                ivals = interpolate(start, end, n, rounding_style = iround)

                # insert interpolated values into sequence
                for ival in ivals:
                    seq.append(ival)

    elif size < steps:
        # trim end of sequence
        seq = seq[:size]

    return seq

def contract_seq(seq: list, size: int, style: int|str = 0, looplen = 0, iround = "none"):
    "Alias for expand_seq()"
    return expand_seq(seq, size, style, looplen, iround)

def reverse_seq(seq: list):
    "Reverse sequence"
    return list(reversed(seq))

def loop_seq(seq: list, n: int = 2):
    "Copy sequence n times"

    if not n: return []

    is_neg = n < 0
    n = abs(n)
    size = rounder(len(seq) * n)

    seq = expand_seq(seq, size, 'loop')

    if is_neg:
        seq = reverse_seq(seq)

    return seq

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
    if shift: coll = shift_seq(coll, shift)

    return coll

# Base Class code

class SequenceBase(ABC, MutableSequence):
    """
    Abstract base class representing a skeleton sequence.
    """

    def __init__(self, sequence: Optional[list] = None):
        self.steps = 0
        self.hits = 0
        self.offset = 0
        self.seq = []

    # Sequence creation

    @abstractmethod
    def set(self, sequence: Optional[list|int|SequenceBase] = None):
        """
        Set sequence, including getting number of steps and hits, and zeroing offset
        """
        pass

    @abstractmethod
    def copy(self):
        """ Copy sequence """
        pass

    # Sequence manipulation

    @abstractmethod
    def insert(self, sequence, step: int = 1):
        """ Insert a sequence into sequence """
        pass

    @abstractmethod
    def remove(self, *args: int):
        """ Remove part of sequence """
        pass

    @abstractmethod
    def append(self, sequence):
        """ Append sequence to end """

    @abstractmethod
    def prepend(self, sequence):
        """Prepend sequence to start"""
        pass

    @abstractmethod
    def replace(self, sequence, step: int = 1, style: Optional[str] = None):
        """Replace portion of sequence"""
        pass

    @abstractmethod
    def shift(self, amount: int = DEFAULT_SHIFT, style: Optional[str] = None):
        """Shift sequence"""
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def stretch_by(self, mult: Optional[int|float] = 2, style: Optional[int|str] = -1,
        *,
        interpolate_style: Optional[str] = None,
        interpolate_rounding: Optional[str] = None,
        mult_rounding: Optional[str] = None
    ):
        """Stretch sequence by multiplier, creating/removing intermediate values"""
        pass

    @abstractmethod
    def shrink_to(self, *args, **kwargs):
        """Alias for stretch_to()"""
        pass

    @abstractmethod
    def shrink_by(self, div: Optional[int|float] = 2, *args, **kwargs):
        """Reverse of stretch_by() (as in will divide instead of multiply)"""
        pass

    @abstractmethod
    def expand_to(self, size: Optional[int], style: Optional[int|str] = -1,
                  *,
                  loop_length: Optional[int] = None,
                  interpolate_rounding: Optional[str] = None
    ):
        """Expand sequence to size, adding/removing values at end"""
        pass

    @abstractmethod
    def expand_by(self, mult: Optional[int|float] = 2, style: Optional[int|str] = -1,
                  *,
                  mult_rounding: Optional[str] = None,
                  **kwargs
    ):
        """Expand sequence by multiplier, adding/removing values at end"""
        pass

    @abstractmethod
    def contract_to(self, *args, **kwargs):
        """Alias for expand_to()"""
        pass

    @abstractmethod
    def contract_by(self, div: Optional[int|float] = 2, *args, **kwargs):
        """Reverse of expand_by() (as in will divide instead of multiply)"""
        pass

    @abstractmethod
    def reverse(self):
        """Reverse sequence"""
        pass

    @abstractmethod
    def loop(self, n: int = 2):
        """Copy sequence n times"""
        pass

    ## Step/value manipulation

    @abstractmethod
    def replace_value(self, value: int, rvalue: int, limit: int = 0):
        """Replace specified value in sequence with another value"""
        pass

    @abstractmethod
    def replace_step(self, step: int, value: int = 0):
        """Replace value at step with specified value"""
        pass

    ## Manipulation magic methods

    def __add__(self, other: Sequence|list):
        """
        Return new sequence consisting of second sequence appended to first.
        """
        seq = self.copy()

        match other:
            case list():
                seq.set(self.seq + other)
            case Sequence():
                seq.set(self.seq + other.seq)

        return seq

    def __mul__(self, n: int):
        """
        Return new sequence consisting of sequence looped n times.
        """
        return self.copy().loop(n)

    def __truediv__(self, n):
        """
        Returns new sequence shrunk by n
        """
        return self.copy().shrink_by(n)

    def __floordiv__(self, n):
        """
        Returns new sequence contracted by n
        """
        return self.copy().contract_by(n)

    # Sequence querying

    def as_list(self):
        """Get sequence as list"""
        return self.seq

    def __call__(self):
        """
        Alias for as_list()
        """
        return self.as_list()

    def __len__(self):
        """Sequence length"""
        return self.steps

    def __getitem__(self, step: int):
        """Get step by bracket notation"""
        return self.seq[step - 1]

    def __setitem__(self, step: int, value: int):
        """Set step by bracket notation"""
        self.replace_step(step, value)

    @abstractmethod
    def __delitem__(self, step: int):
        """
        Delete an item
        """
        pass

    def __iter__(self):
        """Iterate over hits"""
        return (i for i in self.seq)

    def __eq__(self, other: SequenceBase|list):
        "Test if sequences are the same"
        s1 = self.seq
        s2 = other if type(other) == list else other.seq
        return s1 == s2

    # String representation

    def __repr__(self):
        return f'{self.__class__}({self.seq})'

    def __str__(self):
        return f'{self.steps}:{self.hits} {self.seq}'
