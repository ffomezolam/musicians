""" sequence_group.py
---------------------
Functions and classes for managing collections of sequences
"""

from __future__ import annotations
from typing import Optional

from sequence import Sequence
from opts import OptsMixin

# Defaults

from sequence_defaults import *

# Helper functions

def list_has_type(type, l: list):
    """
    Helper function to see if list elements are of a single type.
    Helpful advice from https://stackoverflow.com/questions/13252333/check-if-all-elements-of-a-list-are-of-the-same-type
    """
    return all(isinstance(i, type) for i in l)

def list_type(l: list):
    """ Helper function t get type of elements in list. Returns None if mixed types. """
    types = set()
    for i in l: types.add(type(i))

    return types.pop() if len(types) == 1 else None

# Class definition

class SequenceGroup(OptsMixin):
    """
    A group of sequences that works as a unit
    """

    def __init__(self, seqs: list[Sequence]|dict, labels: Optional[list] = None,
                 *,
                 options: Optional[dict] = None):
        self.steps = 0
        self.hits = 0
        self.offset = 0

        self.seqs = []
        self.labels = {}

        # self._opts pulled in by OptsMixin
        OptsMixin.__init__(DEFAULT_SEQUENCEGROUP_OPTS | DEFAULT_SEQUENCE_OPTS)

        self.setopts(options)

        self.add(seqs, labels)

    def add(self, seqs: dict|list[Sequence|list|int]|Sequence, labels: Optional[list|str] = None):
        """
        Add sequence(s) to group

        Parameters
        ----------
        seqs: dict|list|Sequence
            If dict, a dictionary of label-sequence pairs to add
            If list, a sequence or list of sequences to add.
            If Sequence, a sequence to add
        labels: [list|str]
            If seqs is passed a list, this allows labels to be passed as well.
            If seqs is passed a single sequence, this is the sequence label
            By default labels will just be increasing numbers.
        """

        if type(seqs) is Sequence:
            if not labels or type(labels) != str:
                labels = len(self.seqs)
        else:
            if type(seqs) == dict:
                # get labels and seqs from dict
                l, s = list(zip(*seqs.items()))

                # add labels and seqs as lists
                return self.add(list(s), list(l))

            elif type(seqs) == list:
                match list_type(seqs):
                    # Unfortunately we need to namespace these or it won't work.
                    # Not the end of the world, but doesn't look nice
                    case __main__.Sequence:
                        # list of Sequences
                        pass
                    case __builtins__.list:
                        # list of lists
                        pass
                    case __builtins__.int:
                        # a single sequence as a list: convert to Sequence
                        pass

    def __getitem__(self, label):
        """
        Bracket notation gets sequence with label
        """
        pass

    def __setitem(self, label, seq):
        """
        Bracket notation for setting sequence at label
        """
        pass
