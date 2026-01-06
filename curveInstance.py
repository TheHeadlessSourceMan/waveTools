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
    def timedelta(self)->datetime.timedelta:
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

    def getWindow(self,
        startTime:typing.Union[None,datetime.datetime,datetime.timedelta]=None,
        endTime:typing.Union[None,datetime.datetime,datetime.timedelta]=None,
        maxTime:typing.Union[None,datetime.datetime,datetime.timedelta]=None
        )->"CurveInstance":
        """
        Cut this into a window

        NOTE: since this is always guranteed to return a non-infinite curve,
        if the curve will be infinite, this will use a fallback maxTime of 1second
        """
        if startTime is None:
            startTime=self.startTime
        elif isinstance(startTime,datetime.timedelta):
            startTime=self.startTime+startTime
        if endTime is None:
            endTime=self.endTime
        elif isinstance(endTime,datetime.timedelta):
            endTime=self.startTime+endTime
        if maxTime is None:
            maxTime=self.endTime
        elif isinstance(maxTime,datetime.timedelta):
            maxTime=self.startTime+maxTime

    def getPoints(self,
        sampleInterval:datetime.timedelta,
        startTime:typing.Union[None,datetime.datetime,datetime.timedelta]=None,
        endTime:typing.Union[None,datetime.datetime,datetime.timedelta]=None,
        maxTime:typing.Union[None,datetime.datetime,datetime.timedelta]=None
        )->typing.Tuple[typing.List[float],typing.List[float]]:
        """
        Etract a discrete series of points
        """
        if startTime is None:
            startTime=self.startTime
        elif isinstance(startTime,datetime.timedelta):
            startTime=self.startTime+startTime
        if endTime is None:
            endTime=self.endTime
        elif isinstance(endTime,datetime.timedelta):
            endTime=self.startTime+endTime
        if maxTime is None:
            maxTime=self.endTime
        elif isinstance(maxTime,datetime.timedelta):
            maxTime=self.startTime+maxTime
        x=[]
        y=[]
        t=startTime
        while t<endTime:
            x.append(t)
            y.append(self.getValueAt(t))
            t+=sampleInterval
        return (x,y)

    def getPlot(self,
        startTime:typing.Union[None,datetime.datetime,datetime.timedelta]=None,
        endTime:typing.Union[None,datetime.datetime,datetime.timedelta]=None,
        maxTime:typing.Union[None,datetime.datetime,datetime.timedelta]=None):
        """
        get a matplotlib plot of this curve

        :maxTime: is useful in case the curve is infinite
            If the curve is infinite and there is no maxTime specified
            then the curve will be clamped to 1second,
            which may not be what you want.
        """
        import matplotlib.pyplot as plt
        if startTime is None:
            startTime=self.startTime
        elif isinstance(startTime,datetime.timedelta):
            startTime=self.startTime+startTime
        if endTime is None:
            endTime=self.endTime
        elif isinstance(endTime,datetime.timedelta):
            endTime=self.startTime+endTime
        # TODO: calculate sampleInterval based on desired output size
        sampleInterval=(endTime-startTime)/100
        xs,ys=self.getPoints(sampleInterval,startTime,endTime,maxTime)
        # Create figure without displaying it
        fig,ax=plt.subplots()
        ax.plot(xs,ys)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Point Plot")
        return fig,plt

    def getPlotImage(self,
        startTime:typing.Union[None,datetime.datetime,datetime.timedelta]=None,
        endTime:typing.Union[None,datetime.datetime,datetime.timedelta]=None,
        maxTime:typing.Union[None,datetime.datetime,datetime.timedelta]=None):
        """
        get a pil image of this curve

        :maxTime: is useful in case the curve is infinite
            If the curve is infinite and there is no maxTime specified
            then the curve will be clamped to 1second,
            which may not be what you want.
        """
        from PIL import Image
        import io
        fig,plt=self.getPlot(startTime,endTime,maxTime)
        buf=io.BytesIO()
        fig.savefig(buf,format='png',bbox_inches='tight')
        plt.close(fig)  # close figure to avoid memory leaks
        buf.seek(0)
        # Convert buffer to PIL image
        img=Image.open(buf)
        return img

    def viewPlot(self,
        startTime:typing.Union[None,datetime.datetime,datetime.timedelta]=None,
        endTime:typing.Union[None,datetime.datetime,datetime.timedelta]=None,
        maxTime:typing.Union[None,datetime.datetime,datetime.timedelta]=None):
        """
        view a plot of this curve

        :maxTime: is useful in case the curve is infinite
            If the curve is infinite and there is no maxTime specified
            then the curve will be clamped to 1second,
            which may not be what you want.
        """
        im=self.getPlotImage(startTime,endTime,maxTime)
        im.show()
