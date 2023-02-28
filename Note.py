""" Note.py
-----------
Class representing a musical note and helper functions for working with note
data
"""

from __future__ import annotations
from typing import Optional

# Instance option methods

from opts import OptsMixin

# defaults

from note_defaults import DEFAULT_NOTE_OPTS

class Note(OptsMixin):
    """
    Represents a musical note
    """

    def __init__(self, pitch, velocity, duration,
                 *,
                 options: Optional[dict] = None
    ):
        self.pitch = pitch
        self.velocity = velocity
        self.duration = duration

        OptsMixin.__init__(self, DEFAULT_NOTE_OPTS)
        self.setopts(options)
