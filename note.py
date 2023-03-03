""" note.py
-----------
Class representing a musical note and helper functions for working with note
data
"""

from __future__ import annotations
from typing import Optional

# defaults

from note_defaults import DEFAULT_PITCH, DEFAULT_VELOCITY, DEFAULT_DURATION
from note_defaults import DEFAULT_NOTE_OPTS

# Supporting classes

from pitch import Pitch
from duration import Duration

# Note class

class Note():
    """
    Represents a musical note
    """

    def __init__(self,
                 pitch: Optional[int|str|Pitch|Note] = None,
                 velocity: Optional[int] = None,
                 duration: Optional[int|str|Duration] = None
    ):
        self.pitch = None
        self.velocity = None
        self.duration = None

        self.set(pitch, velocity, duration)

    def set(self,
            pitch: Optional[int|str|Pitch|Note] = None,
            velocity: Optional[int] = None,
            duration: Optional[int|str|Duration] = None
    ):
        match pitch:
            case int() | str() | Pitch():
                pass
            case _:
                self.pitch = DEFAULT_PITCH

        match velocity:
            case _:
                self.velocity = DEFAULT_VELOCITY

        match duration:
            case _:
                self.duration = DEFAULT_DURATION

    # String representation

    def __repr__(self):
        pass

    def __str__(self):
        pass
