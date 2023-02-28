""" Pitch.py
-----------
Class representing a musical pitch and helper functions for working with pitch
data
"""

from __future__ import annotations
from typing import Optional

# Instance option methods

from opts import OptsMixin

# Defaults

from pitch_defaults import MIDDLE_C_OCTAVE, DEFAULT_NOTE, DEFAULT_OCTAVE

# Pitch class

class Pitch(OptsMixin):
    """
    Represents a musical pitch
    """

    def __init__(self,
                 note: Optional[str|int] = None,
                 octave: Optional[int] = None,
                 *,
                 options: Optional[dict] = None
    ):
        self.note = None
        self.octave = None

        OptsMixin.__init__(self, DEFAULT_PITCH_OPTS)
        self.setopts(options)

        self.set(note, octave)

    def set(self, note: str|int = DEFAULT_NOTE, octave: int = DEFAULT_OCTAVE):
        """
        Set pitch value by note and octave.
        Can pass int to `note` argument to directly set pitch value.
        """
