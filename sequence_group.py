""" sequence_group.py
---------------------
Functions and classes for managing collections of sequences
"""

from __future__ import annotations
from typing import Optional

from sequence import Sequence

# Defaults

from sequence_defaults import *

# Helper functions

# Class definition

class SequenceGroup():
    """
    A group of sequences that works as a unit
    """

    def __init__(self,
                 seqs: list[Sequence]|dict,
                 labels: Optional[list] = None
    ):
        self.seqs = {}

        self.add(seqs, labels=labels)

    def add(self, seqs: list[Sequence]|dict, labels: Optional[list] = None):
        """
        Add sequences to group

        Parameters
        ----------
        seqs: list|dict
            If list, a list of sequences to add.
            If dict, a dictionary of label-sequence pairs
        labels: [list]
            If seqs is passed a list, this allows labels to be passed as well.
            By default labels will just be increasing numbers.
        """
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
