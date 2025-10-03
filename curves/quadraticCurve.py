"""
A basic quadratic curve
"""
import typing
import numpy as np
from .curveBase import (
    CurveBase,asCurve,CurveValueT,CurveTimeValue,CurveCompatible)


def asQuadraticCurve(curve:CurveCompatible,order:int=1):
    """
    Create a QuadraticCurve from the data given.

    If it is already a QuadraticCurve, return it.
    Otherwise, fit a QuadraticCurve to the data.
    """
    if isinstance(curve,QuadraticCurve):
        return curve
    curve=asCurve(curve).samples()
    x=np.array(range(len(curve)))
    coeffients=np.polyfit(x,curve,deg=order)
    return QuadraticCurve(coeffients)


class QuadraticCurve(CurveBase[CurveValueT]):
    """
    A basic quadratic curve
    """
    def __init__(self,
        coeffients:np.ndarray):
        """ """
        self.coeffients=coeffients

    @property
    def start(self)->CurveTimeValue:
        """
        Start time of the curve
        """
        return float("-Inf")

    @property
    def end(self)->CurveTimeValue:
        """
        End time of the curve
        """
        return float("Inf")

    @property
    def order(self)->int:
        """
        What order curve is this
        """
        return len(self.coeffients)

    def solve(self,x:np.ndarray)->np.ndarray:
        """
        Solve the function for a given x
        """
        poly=np.poly1d(self.coeffients)
        return poly(x)
    __call__=solve

    def valueAt(self,position:CurveTimeValue)->CurveValueT:
        """
        Get value at a given point
        """
        return self.solve(position)

    def samples(self,
        start:typing.Optional[CurveTimeValue]=None,
        stop:typing.Optional[CurveTimeValue]=None,
        step:CurveTimeValue=1
        )->np.ndarray:
        """
        Get a block of samples
        """
        return self.solve(np.array(range(start,stop,step)))
LinearCurve=QuadraticCurve
