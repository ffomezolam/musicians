""" sequence_defaults.py
------------------------
Default settings for sequencer modules
"""

# TODO: Restructure as an Enum class?

# default number of steps in a sequence
DEFAULT_STEPS = 16

# default number of hits in a sequence
DEFAULT_HITS = 4

# default shift amount of sequence
DEFAULT_SHIFT = 0

# default sequence options
DEFAULT_OPTS = {
    # how to handle shifting sequences
    "shift-style": "relative", # "relative", "absolute"

    # how to handle stretching sequences
    "stretch-with": 0, # int fills with value, "repeat" each hit, "interpolate"

    # how to handle expanding sequences
    "expand-with": 0, # int fills with value, "repeat" last value, "loop" sequence, "interpolate" to start

    # how to handle replacement where replacement bounds exceed sequence length
    "replace-style": "expand", # "trim" trims input to length, "expand" expands to fit all

    # how to handle interpolation of final hits
    "interpolate-style": "loop", # "repeat" last value, "loop" to first value

    # whether to round interpolation results
    "interpolate-rounding": "none", # "none", "auto", "up", "down"

    # how to round numbers generally when rounding is necessary
    "global-rounding": "auto", # "auto", "up", "down"

    # length of loop when looping
    "loop-length": 0, # 0 for entire loop, int for last n items
}

# initial group labels
DEFAULT_GROUP_LABELS = ['gate', 'pitch', 'velocity']
