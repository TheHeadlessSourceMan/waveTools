"""
A basic gaussian curve
"""
import numpy as np
from .curveBase import CurveBase,CurveValueT,CurveTimeValue


SQRT_2PI=np.sqrt(2*np.pi)


class GaussianCurve(CurveBase[CurveValueT]):
    """
    A basic gaussian curve
    """
    def __init__(self,mean:CurveValueT,stdev:CurveValueT):
        self._mean=mean
        self._stdev=stdev

    @property
    def start(self)->CurveValueT:
        """
        start is the -stdev
        """
        return -self.stdev

    @property
    def end(self)->CurveValueT:
        """
        end is the stdev
        """
        return self.stdev

    @property
    def timeShift(self)->CurveValueT:
        """
        end is the stdev
        """
        return self.stdev

    def valueAt(self,position:CurveTimeValue)->CurveValueT:
        """
        Get value at a given point
        """
        exponent=-((position-self.mean)**2)/(2*self.stdev**2)
        return self.coefficient*np.exp(exponent)

    @property
    def coefficient(self)->CurveValueT:
        """
        Coefficient of the gaussian distribution
        """
        return 1/(self.stdev*SQRT_2PI)
    @coefficient.setter
    def coefficient(self,coefficient:CurveValueT):
        self.stdev=SQRT_2PI/coefficient

    @property
    def stdev(self)->CurveValueT:
        """
        Standard deviation
        """
        return self._stdev

    @property
    def mean(self)->CurveValueT:
        """
        Arithmatic mean
        """
        return self._mean
