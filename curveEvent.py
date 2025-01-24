"""
An event that kicks off a curve

This can be used for things like kicking off a
sequence of events that follow a particular
curve pattern.

TODO: this is only a brainstorm and
needs to be thought through more
"""
import typing
import datetime
from .curveShape import CurveShape
from .curveInstance import CurveInstance


class CurveEvent:
    """
    An event that kicks off a curve

    This can be used for things like kicking off a
    sequence of events that follow a particular
    curve pattern.

    TODO: this is only a brainstorm and
    needs to be thought through more
    """

    def __init__(self,
        curve:CurveShape,
        onCurveStarted:typing.Optional[typing.Callable]=None):
        """ """
        self.curve=curve
        self.onCurveStarted=onCurveStarted

    def onEventOccoured(self,
        startTime:typing.Optional[datetime.datetime]
        )->typing.Union[CurveInstance,typing.Any]:
        """
        Call this when a curve event starts.

        if onCurveStarted is set, call it and return the result
        otherwise, return a new CurveInstance
        """
        curveInstance=self.curve.startInstance(startTime)
        if self.onCurveStarted is not None:
            return self.onCurveStarted(curveInstance)
        return curveInstance
