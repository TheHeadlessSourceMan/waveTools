"""
Base class for any type of abstract curve
"""
import typing
from abc import abstractmethod
import datetime
from .curveValueT import CurveValueT
from .endTreatment import END_TREATMENT
if typing.TYPE_CHECKING:
    from curveInstance import CurveInstance


class CurveShape(typing.Generic[CurveValueT]):
    """
    Base class for any type of abstract waveform curve

    The idea is there is a waveform where you can use indexing to get
    a value at a particular point,for instance,waveform[10.5]
    or you can also get an array waveform[10.5;12.5]
    or if you don't care about all values,you can waveform.range(10.5,0.5,11.5)
    """

    def __init__(self,
        atStart:END_TREATMENT=END_TREATMENT.CLAMP,
        atEnd:END_TREATMENT=END_TREATMENT.CLAMP):
        """ """
        self.atStart:END_TREATMENT=atStart
        self.atEnd:END_TREATMENT=atEnd

    @typing.overload
    def __getitem__(self,idx:float)->CurveValueT: ...
    @typing.overload
    def __getitem__(self,idx:typing.Iterable[float])->typing.List[CurveValueT]: ...
    def __getitem__(self,
        idx:typing.Union[float,typing.Iterable[float]]
        )->typing.Union[CurveValueT,typing.List[CurveValueT]]:
        if isinstance(idx,typing.Iterable):
            return [x for x in self.iterate(idx)]
        return self.get(idx)

    def __iter__(self)->typing.Generator[CurveValueT,None,None]:
        return self.range()

    def range(self,start:float=0.0,step:float=1.0,stop:float=0.0
        )->typing.Generator[CurveValueT,None,None]:
        """
        Iterate over a series of x points and return their corresponding y points
        """
        return self.iterate(range(start,step,stop))

    def iterate(self,itr:typing.Iterable[float]
        )->typing.Generator[CurveValueT,None,None]:
        """
        Iterate over a series of x points and return their corresponding y points
        """
        for idx in itr:
            yield self[idx]

    def get(self,idx:float)->CurveValueT:
        """
        Get a single value
        """
        if self.atEnd==END_TREATMENT.NONE:
            return None # type: ignore
        if self.atEnd==END_TREATMENT.INDEX_ERROR:
            raise IndexError()
        return 0 # type: ignore

    @abstractmethod
    def getValueAt(self,relativeTime:float)->CurveValueT:
        """
        get the value of the curve at a particular point in time
        """
        raise NotImplementedError()

    @property
    def duration(self)->float:
        """
        How long does the curve last (in seconds)

        (can return float('inf'))
        """
        return float('inf')

    @property
    def timedelta(self)->float:
        """
        How long does the curve last, as a timedelta

        raises exception if there is no end to this waveform
        """
        duration=self.duration
        if duration==float('inf'):
            raise ValueError('There is no size for an infinite waveform')
        return datetime.timedelta(seconds=duration)

    @property
    def isInfinite(self)->bool:
        """
        does this wave have an end point?
        """
        return self.duration==float('inf')

    @property
    def hasEndpoint(self)->bool:
        """
        does this wave have an end point?
        """
        return self.duration!=float('inf')

    def startCurveInstance(self,
        startTime:typing.Optional[datetime.datetime]
        )->"CurveInstance[CurveValueT]":
        """
        Create a new instance of this particular curve
        """
        from curveInstance import CurveInstance
        return CurveInstance[CurveValueT](self,startTime)
