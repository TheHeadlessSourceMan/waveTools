"""
Spline curve
can form the basis of many types of curves
"""
import typing
import numpy as np
from scipy.interpolate import UnivariateSpline
from .curveBase import CurveBase,CurveValueT,CurveTimeValue
from .percent import PercentCompatible


class SplineCurve(CurveBase[CurveValueT]):
    """
    Spline curve
    can form the basis of many types of curves
    """
    def __init__(self,
        controlPoints:typing.Union[
            typing.Iterable[typing.Iterable[int]],
            np.ndarray[int,CurveValueT]]):
        """ """
        if not isinstance(controlPoints,np.ndarray):
            controlPoints=np.array(controlPoints)
        self._controlPoints=controlPoints
        if len(self._controlPoints.shape)<2:
            x=np.ndarray(range(len(self._controlPoints)))
            y=self._controlPoints
            s=1
        else:
            x=self._controlPoints[0]
            y=self._controlPoints[1]
            s=0
        self._spline=UnivariateSpline(x,y,s=s)

    def samples(self,
        start:typing.Optional[CurveTimeValue]=None,
        stop:typing.Optional[CurveTimeValue]=None,
        step:CurveTimeValue=1
        )->np.ndarray:
        """
        Get a block of samples
        """
        if start is None and stop is None:
            return self.samples()
        return np.array(
            self.valueAt(position) for position in range(start,stop,step))

    @property
    def start(self)->CurveValueT:
        """
        start index
        """
        return self._controlPoints[0][0]

    @property
    def end(self)->CurveValueT:
        """
        end index
        """
        return self._controlPoints[-1][0]

    def _apply(self,
        other:typing.Union[CurveBase[CurveValueT],float,int],
        func:typing.Callable[[np.ndarray],np.ndarray]
        )->"SplineCurve[CurveValueT]":
        """
        """
        if isinstance(other,(float,int)):
            result_samples=func(self.samples(),other)
        elif isinstance(other,SplineCurve):
            result_samples=func(self.samples(),other.samples())
        elif hasattr(other,'toSpline'):
            other=other.toSpline()
            result_samples=func(self.samples(),other.samples())
        else:
            raise TypeError(f"Unsupported operation with {type(other)}")
        return SplineCurve[CurveValueT](result_samples)

    def valueAt(self,position:CurveTimeValue)->CurveValueT:
        """
        Get value at a given point
        """
        return self._spline(position)

    def __add__(self,other):
        return self._apply(other,np.add)

    def __sub__(self,other):
        return self._apply(other,np.subtract)

    def __mul__(self,other):
        return self._apply(other,np.multiply)

    def __truediv__(self,other):
        return self._apply(other,np.divide)

    def toSpline(self,
        percentError:PercentCompatible=1.0
        )->"SplineCurve[CurveValueT]":
        """
        Redundant, but necessary for compatability
        """
        _=percentError # it will always be a 100% fit
        return self
