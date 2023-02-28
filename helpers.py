""" helpers.py
--------------
Miscellaneous helper functions
"""

from typing import Optional

import math

# Helper functions

def mod(a, b):
    """
    Helper function for alternative modulo operations on negative numbers.
    From https://stackoverflow.com/questions/3883004/how-does-the-modulo-operator-work-on-negative-numbers-in-python
    """
    r = a % b
    return r - b if a < 0 else r

def rounder(n, style: str = "auto"):
    "Various rounding styles"
    match style:
        case "auto":
            return int(n + 0.5)
        case "up":
            return math.ceil(n)
        case "down":
            return math.floor(n)
        case _:
            return n

def interpolate(val1, val2, num: Optional[int] = 1, func = "linear", rounding_style: str = "none"):
    """Interpolate num values between val1 and val2"""

    if val1 == val2: return [val1 for _ in range(num)]

    mult = (val2 - val1) / (num + 1)

    return [rounder(val1 + (mult * i), rounding_style) for i in range(1, num + 1)]
