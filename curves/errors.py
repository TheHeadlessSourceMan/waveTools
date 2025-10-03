"""
Errors for these classes
"""

class NumberException(Exception):
    """
    A general number-related exception
    """

class CurveException(NumberException):
    """
    A general exception that has to do with curves
    """

class NonDiscreteCurveException(CurveException):
    """
    Attempt to perform a discrete action on
    a curve that is non-discrete.
    (The types of curves your mother warned you about!)

    For instance, how long is a sine wave?
    Doesn't make sense. It goes on as long as you need it to.
    """
