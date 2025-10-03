"""
Common base class for all curves
"""
import typing
from abc import abstractmethod
import numpy as np
from .percent import PercentCompatible,asPercent
from .errors import NonDiscreteCurveException
if typing.TYPE_CHECKING:
    from splineCurve import SplineCurve


class NumberLike(typing.Protocol):
    """
    TODO:I have a better implementaion of this elsewhere
    """

CurveCompatible=typing.Union[
    float,int,
    np.ndarray,
    "CurveBase",
    typing.Iterable["CurveCompatible"]]

def asCurve(curve:CurveCompatible):
    """
    Create a curve from the data given.

    If it is already a curve, return it.
    Otherwise, create a DiscretePointCurve
    to wrap it.
    """
    if isinstance(curve,CurveBase):
        return curve
    from .discretePointCurve import DiscretePointCurve
    return DiscretePointCurve(curve)

CurveTimeValue=float

CurveValueT=typing.TypeVar("CurveValueT",bound=NumberLike)
class CurveBase(typing.Generic[CurveValueT]):
    """
    Common base class for all curves
    """
    @property
    def length(self)->CurveTimeValue:
        """
        how long the timespan of the curve is
        """
        if not self.isDiscrete:
            return float('Inf')
        return self.end-self.start
    @length.setter
    def length(self,length:CurveTimeValue):
        self.end=self.start+length

    @property
    def start(self)->CurveTimeValue:
        """
        Start time of the curve
        """
        return 0

    @property
    def end(self)->CurveTimeValue:
        """
        End time of the curve
        """
        return float("Inf")

    @property
    def timeShift(self)->CurveTimeValue:
        """
        End time of the curve
        """
        return 0

    @property
    def isDiscrete(self)->bool:
        """
        Is this curve limited to
        a discrete range of time
        """
        return self.start!=float("-Inf") \
            and self.end!=float("Inf")

    @property
    def stdev(self)->float:
        """
        Standard deviation
        """
        return np.std(self.samples())

    @property
    def mean(self)->float:
        """
        Arithmatic mean
        """
        return np.mean(self.samples())

    @property
    def cov(self)->CurveValueT:
        """
        Coeffiencent of Variation
        """
        return self.mean/self.stdev

    def correlate(self,other:CurveCompatible)->float:
        """
        Compare with another curve and return an r-squared value
        """
        return np.correlate(self.samples(),asCurve(other).samples())

    def compare(self,other:CurveCompatible)->float:
        """
        Compare with another curve and return an r-squared value
        """
        self.correlate(other)
    def rSquared(self,other:CurveCompatible)->float:
        """
        Compare with another curve and return an r-squared value
        """
        self.correlate(other)

    @abstractmethod
    def valueAt(self,position:CurveTimeValue)->CurveValueT:
        """
        Get value at a given point
        """
    def at(self,position:CurveTimeValue)->CurveValueT:
        """
        Get value at a given point
        """
        return self.valueAt(position)

    def samples(self,
        start:typing.Optional[CurveTimeValue]=None,
        stop:typing.Optional[CurveTimeValue]=None,
        step:CurveTimeValue=1
        )->np.ndarray:
        """
        Get a block of samples
        """
        if start is None:
            if self.start==float('-Inf'):
                raise NonDiscreteCurveException('Cannot calculate all points of an infinite curve. (Need to specify a start for this to work)') # noqa: E501 # pylint: disable=line-too-long
            start=self.start+self.timeShift
        if stop is None:
            if self.end==float('Inf'):
                raise NonDiscreteCurveException('Cannot calculate all points of an infinite curve. (Need to specify an end for this to work)') # noqa: E501 # pylint: disable=line-too-long
            stop=self.end+self.timeShift
        return np.array(
            self.at(position) for position in range(start,stop,step))

    def __gititem__(self,idx:CurveTimeValue)->CurveValueT:
        """
        Access like an array of values
        """
        return self.valueAt(idx)

    def __iter__(self)->typing.Iterable[CurveValueT]:
        if not self.isDiscrete:
            raise NonDiscreteCurveException("It is a bad idea to iterate over an infinite curve") # noqa: E501 # pylint: disable=line-too-long
        return iter(self.at(position) for position in range(self.end))

    def __len__(self)->CurveTimeValue:
        if not self.isDiscrete:
            raise NonDiscreteCurveException("This curve is infinite") # noqa: E501 # pylint: disable=line-too-long
        return self.length

    @property
    def min(self)->CurveValueT:
        """
        The minimum value
        """
        return np.min(self.samples())

    @property
    def max(self)->CurveValueT:
        """
        The maximum value
        """
        return np.max(self.samples())

    @property
    def valueRange(self)->typing.Tuple[CurveValueT,CurveValueT]:
        """
        The range of values (min,max)
        """
        return self.min,self.max

    @property
    def rangeAmount(self)->CurveValueT:
        """
        The spread amount of the value range
        """
        return self.max-self.min

    def toSpline(self,
        percentError:PercentCompatible=0.80
        )->"SplineCurve":
        """
        Convert to a spline curve

        Used as a standard fallback for math operations
        """
        percentError=asPercent(percentError)
        from scipy.interpolate import UnivariateSpline
        from .splineCurve import SplineCurve
        # convert from percent error to S
        x=np.array(range(len(self.samples())))
        allowedDeviation=percentError*self.rangeAmount
        s=len(self.samples())*(allowedDeviation**2)
        # create the spline
        spline=UnivariateSpline(x,self.samples(),s=s)
        return SplineCurve(spline)
