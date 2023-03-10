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
                 duration: Optional[int|str|Duration] = None,
                 velocity: Optional[int] = None
    ):
        self.pitch = None
        self.duration = None
        self.velocity = None

        self.set(pitch, duration, velocity)

    def set(self,
            pitch: Optional[int|str|Pitch|Note] = None,
            duration: Optional[int|str|Duration] = None,
            velocity: Optional[int] = None
    ):
        "Set Note attributes"

        match pitch:
            case int() | str() | Pitch():
                self.pitch = Pitch(pitch)
            case Note():
                self.pitch = pitch.pitch.copy()
                self.velocity = pitch.velocity
                self.duration = pitch.duration.copy()
            case _:
                self.pitch = DEFAULT_PITCH

        match duration:
            case int():
                self.duration = duration
            case _:
                self.duration = DEFAULT_DURATION

        match velocity:
            case int():
                self.velocity = velocity
            case _:
                self.velocity = DEFAULT_VELOCITY

        return self

    def copy(self):
        "Make a copy of Note"

        return Note(self)

    # String representation

    def as_str(self):
        "Pretty printing"
        return f'{self.pitch}, {self.duration}, v{self.velocity}'

    def __repr__(self):
        return f'{self.__class__}({self.pitch, self.duration, self.velocity})'

    def __str__(self):
        return self.as_str()

class Rest(Note):
    "Represents a rest (a note with velocity 0)"

    def __init__(self, duration: Optional[int|str|Duration] = None):
        Note.__init__(self, 0, duration, 0)
