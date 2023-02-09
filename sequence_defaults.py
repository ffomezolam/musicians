""" sequence_defaults.py
------------------------
Default settings for sequencer modules
"""

DEFAULT_STEPS = 16
DEFAULT_SHIFT = 0
DEFAULT_HITS = 4
DEFAULT_OPTS = {
    "shift-style": "relative", # "relative", "absolute"
    "stretch-with": 0, # int fills with value, "repeat" each hit, "interpolate"
    "expand-with": 0, # int fills with value, "repeat" last value, "loop" sequence, "interpolate" to start
    "replace-style": "expand", # "trim" trims input to length, "expand" expands to fit all
    "interpolate-style": "loop", # "repeat" last value, "loop" to first value
    "interpolate-rounding": "none", # "none", "auto", "up", "down"
    "global-rounding": "auto", # "auto", "up", "down"
    "loop-length": 0, # 0 for entire loop, int for last n items
}
