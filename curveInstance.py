"""
A Curve shape with a definite start time
"""
import typing
import datetime
from .curveValueT import CurveValueT
from .curveShape import CurveShape


class CurveInstance(typing.Generic[CurveValueT]):
    """
    A Curve shape with a definite start time in reality

    Usually you create this with:
        curveShapeX.startCurveInstance(t)
    Or you could also do
        CurveInstance(curveShapeX,t)
    """
    def __init__(self,
        curveShape:CurveShape,
        startTime:typing.Optional[datetime.datetime]=None):
        """ """
        self.curveShape=curveShape
        if startTime is None:
            startTime=datetime.datetime.now()
        self.startTime=startTime

    @property
    def duration(self)->float:
        """
        How long does the curve last (in seconds)

        (can return float('inf'))
        """
        return self.curveShape.duration

    @property
    def timedelta(self)->float:
        """
        How long does the curve last, as a timedelta

        raises exception if there is no end to this waveform
        """
        return self.curveShape.timedelta

    @property
    def isInfinite(self)->bool:
        """
        does this wave have an end point?
        """
        return self.curveShape.isInfinite

    @property
    def hasEndpoint(self)->bool:
        """
        does this wave have an end point?
        """
        return self.curveShape.hasEndpoint

    @property
    def endTime(self)->datetime.datetime:
        """
        When will the instance end

        raises exception if there is no end to this waveform
        """
        return self.startTime+self.timedelta

    def getValueAt(self,timestamp:datetime.datetime)->CurveValueT:
        """
        get the value of the curve at a particular point in time
        """
        t=(timestamp-self.startTime).seconds()
        return self.curveShape.getValueAt(t)
