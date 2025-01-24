"""
Curve implementing a parametric sine wave
"""
import typing
import math
from .curveValueT import CurveValueT
from .curveShape import CurveShape


class SineCurve(CurveShape[CurveValueT]):
    """
    Curve implementing a parametric sine wave
    """
    def __init__(self,
        x:float=1,
        t:float=0,
        offset:typing.Optional[CurveValueT]=None):
        """
        In the form x*sin(t)+offset
        """
        self.x=x
        self.t=t
        self.offset=offset

    def getValueAt(self,relativeTime:float)->CurveValueT:
        """
        get the value of the curve at a particular point in time
        """
        val:CurveValueT=math.sin(relativeTime)
        if self.offset is not None:
            val=val+self.offset
        return val
