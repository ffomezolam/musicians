""" sequence_base.py
--------------------
Contains abstract base class for sequences an helpful sequence functions
"""

from __future__ import annotations
from typing import Optional

from abc import ABC, abstractmethod # abstract base class support

import itertools as its

# Defaults

from sequence_defaults import DEFAULT_STEPS, DEFAULT_HITS, DEFAULT_SHIFT

# Helpers

from helpers import mod

# Sequence manipulation functions

def shift_seq(l: list, amt: int = 0):
    """Helper function for shifting a standard python list"""
    if not amt: return l

    amt = -mod(amt, len(l)) # allow for amounts above length

    return l[amt:] + l[:amt]

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

# Abstract Class code

class SequenceBase(ABC):
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
    def set(self, sequence: Optional[list|int|Sequence] = None):
        pass

    @abstractmethod
    def copy(self):
        """ Copy sequence """
        pass

    @abstractmethod
    def insert(self, sequence, beat: int = 1):
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
    def replace(self, sequence, beat: int = 1, style: Optional[str] = None):
        """Replace portion of sequence"""
        pass

    # Sequence manipulation

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

    @abstractmethod
    def reset(self):
        """Reset to original sequence (i.e. undo all)"""
        pass

    @abstractmethod
    def _cache_for(self, new_seq: list):
        """Cache sequence and replace with new_seq"""
        pass

    ## Step/value manipulation

    @abstractmethod
    def replace_value(self, value, rvalue, limit: int = 0):
        """Replace specified value in sequence with another value"""
        pass

    @abstractmethod
    def replace_step(self, step, value):
        """Replace value at step with specified value"""
        pass

    # Sequence querying

    @abstractmethod
    def as_list(self):
        """Get sequence as list"""
        pass

    def __call__(self):
        """ Alias for as_list() """
        return self.as_list()

    def __len__(self):
        """Sequence length"""
        return self.steps

    def __getitem__(self, beat: int):
        """Get step by bracket notation"""
        pass

    def __setitem__(self, beat: int, value: int):
        """Set step by bracket notation"""
        pass

    def __iter__(self):
        """Iterate over hits"""
        pass

    # String representation

    def __repr__(self):
        return f'Sequence({self.seq})'

    def __str__(self):
        return f'{self.steps}:{self.hits} {self.seq}'
