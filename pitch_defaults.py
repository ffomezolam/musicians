""" pitch_defaults.py
------------------------
Default settings for pitch modules
"""

# TODO: Restructure as an Enum class?

MIDDLE_C_OCTAVE = 4
DEFAULT_NOTE = 'C'
DEFAULT_OCTAVE = MIDDLE_C_OCTAVE
DEFAULT_LEAN = 1

MIDI_MIN = 0
MIDI_MAX = 127

# TODO: Might not need below - can do wrap as an int argument
WRAP_RE = r'^wrap-?(\d+)?$'

DEFAULT_PITCH_OPTS = {
    # how to wrap transposed notes if they go beyond midi range
    "wrap-style": "limit" # 'limit', 'wrap<n semitones>'
}
