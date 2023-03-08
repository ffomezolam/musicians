""" sequence.py
---------------
All things Sequencing
"""
# TODO: Need to ensure that a sequence can hold arbitrary structures (e.g. a
# Note instance) and perform all operations adequately

from __future__ import annotations
from typing import Optional

import itertools as its

# Instance option methods

from opts import OptsMixin

# Global defaults

from sequence_defaults import *

# Helper functions

from helpers import mod, rounder, interpolate

# Sequence base class

from sequence_base import SequenceBase

# Sequence manipulation functions

from sequence_base import shift_seq, stretch_seq, expand_seq, reverse_seq, loop_seq

# Generator functions

from sequence_base import generate_euclidean

# Class code

class Sequence(SequenceBase, OptsMixin):
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

    def __init__(self, sequence: Optional[list] = None,
                 *,
                 options: Optional[dict] = None
    ):
        # init base class for steps, hits, offset, and seq
        SequenceBase.__init__(self)

        # from SequenceBase
        # self.steps = 0
        # self.hits = 0
        # self.offset = 0
        # self.seq = []

        self._cache = None

        # self._opts created by OptsMixin
        OptsMixin.__init__(self, DEFAULT_SEQUENCE_OPTS)

        self.setopts(options)
        self.set(sequence)

    # Option handling

    # From OptsMixin class
        # setopts()
        # getopts()

    # Sequence creation

    def set(self, sequence: Optional[list|int|SequenceBase] = None):
        """
        Set sequence, including getting number of steps and hits, and zeroing offset
        """
        if not sequence:
            # set to a blank sequence
            return self.set([0 for _ in range(DEFAULT_STEPS)])
        elif type(sequence) == int:
            # set to a blank sequence with specified steps
            return self.set([0 for _ in range(sequence)])
        elif isinstance(sequence, SequenceBase):
            # copy sequence contents
            return self.set(sequence.seq)
        else:
            self.seq = sequence
            self.steps = len(self.seq)
            self.hits = sum([1 if item > 0 else 0 for item in self.seq])
            self.offset = 0

        return self

    def copy(self):
        """
        Create copy of sequence.

        Overrides SequenceBase.copy() to allow for passing sequence options.
        """
        return Sequence(self.seq, options = self._opts)

    # Sequence manipulation

    def insert(self, sequence: Sequence|list, beat: int = 1):
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

    def shift(self, amount: int = DEFAULT_SHIFT, style: Optional[str] = None):
        """Shift sequence"""

        style = style or self.getopts('shift-style')

        # shift sequence
        if style == 'absolute':
            amount -= self.offset
            self.seq = shift_seq(self.seq, amount)
            self.offset = amount
        else:
            self.seq = shift_seq(self.seq, amount)
            self.offset += amount

        # wrap offset
        self.offset = mod(self.offset, self.steps)

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
        istyle = interpolate_style or self.getopts('interpolate-style')
        iround = interpolate_rounding or self.getopts('interpolate-rounding')

        result = stretch_seq(self.seq, size, style, istyle, iround)
        self._cache_for(result)

        return self

    def stretch_by(self, mult: Optional[int|float] = 2, style: Optional[int|str] = -1,
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

    def shrink_by(self, div: Optional[int|float] = 2, *args, **kwargs):
        """Reverse of stretch_by() (as in will divide instead of multiply)"""

        mult = 1 / div

        return self.stretch_by(mult, *args, **kwargs)

    def expand_to(self, size: Optional[int], style: Optional[int|str] = -1,
                  *,
                  loop_length: Optional[int] = None,
                  interpolate_rounding: Optional[str] = None
    ):
        """Expand sequence to size, adding/removing values at end"""

        # get options
        if style is None or (type(style) == int and style < 0):
            # get default if not set
            style = self.getopts('expand-with')

        # get loop options if style is loop
        if type(style) == str and 'loop' in style:

            if loop_length is None:
                if 'loop-' in style:
                    loop_length = int(style.split('-')[1])
                else:
                    loop_length = self.getopts('loop-length')

            elif loop_length == 0:
                # set loop to entire sequence
                loop_length = self.steps

            style = 'loop'

        interpolate_rounding = interpolate_rounding or self.getopts('interpolate-rounding')

        seq = expand_seq(self.seq, size, style, loop_length, interpolate_rounding)

        # cache and replace
        self._cache_for(seq)

        return self

    def expand_by(self, mult: Optional[int|float] = 2, style: Optional[int|str] = -1,
                  *,
                  mult_rounding: Optional[str] = None,
                  **kwargs
    ):
        """Expand sequence by multiplier, adding/removing values at end"""

        roundmethod = mult_rounding or self.getopts('global-rounding')
        size = rounder(self.steps * mult, roundmethod)

        return self.expand_to(size, style, **kwargs)

    def contract_to(self, *args, **kwargs):
        """Alias for expand_to()"""

        return self.expand_to(*args, **kwargs)

    def contract_by(self, div: Optional[int|float] = 2, *args, **kwargs):
        """Reverse of expand_by() (as in will divide instead of multiply)"""

        mult = 1 / div

        return self.expand_by(mult, *args, **kwargs)

    def reverse(self):
        """Reverse sequence"""

        seq = reverse_seq(self.seq)

        self._cache_for(seq)

        return self

    def loop(self, n: int = 2):
        """Copy sequence n times"""

        seq = loop_seq(self.seq, n)
        self._cache_for(seq)

        return self

    # Caching

    def reset(self):
        """Reset to original sequence (i.e. undo all)"""

        if self._cache:
            self.set(self._cache)
            self._cache = None

        return self

    def _cache_for(self, new_seq: list):
        """Cache sequence and replace with new_seq"""

        if not self._cache: self._cache = self.seq
        self.set(new_seq)

        return self

    ## Step/value manipulation

    def replace_value(self, value, rvalue, limit: int = 0):
        """Replace specified value in sequence with another value"""
        # TODO: This is resetting the whole sequence - what if we want to
        # preserve shift amount, offset, expansion, etc so we can undo those?
        # Probably need to replace value in both seq and cache
        # TODO: implement limit

        self.set([rvalue if step == value else step for step in self.seq])

        return self

    def replace_step(self, step, value):
        """Replace value at step with specified value"""
        # TODO: Same as above - might need to replace something in cache
        # as well

        self[step] = value

        return self

    ### defined by SequenceBase
    # remove_step()

    ## Manipulation magic methods

    ### defined by SequenceBase
    # __add__()
    # __mul__()
    # __truediv__()
    # __floordiv__()
    # __setitem__()

    def __delitem__(self, step: int):
        """ Delete item at step according to delete-style option """

        style = self.getopts("delete-style")

        match style:
            case int():
                self.seq[step] = 0 if style < 0 else style
            case "cut":
                self.remove_step(step)

        return self

    # Sequence querying

    ### defined by SequenceBase class:
    # as_list()
    # __call__()
    # __len__()
    # __getitem__()
    # __iter__()
    # __eq__()

    # String representation

    ### defined by SequenceBase:
    # __repr__()
    # __str__()
