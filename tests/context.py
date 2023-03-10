# taken from The Hitchhiker's Guide To Python

import os
import sys

# add Trieson package path to search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import used modules
import opts
import helpers
import sequence_base
import sequence
import sequence_group
import note
import pitch
import duration
