"""
What to do when indexing past the end of something
"""
from enum import Enum


class END_TREATMENT(Enum):
    """
    What to do when indexing past the end of something
    """
    NONE=0 # return None
    INDEX_ERROR=1 # raise an IndexError exception
    CLAMP=2 # clamp to the last known value
    LOOP=3 # loop back to first value
    REFLECT=4 # reflect and go the other direction
    LINEAR_PROJECTION=5 # project the next value in a linear fashion
    CUBIC_PROJECTION=6 # project the next value in a cubic fashion
