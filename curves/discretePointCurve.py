"""
A basic gaussian curve
"""
import typing
import numpy as np
import scipy.interpolate
from .curveBase import CurveBase,CurveValueT,CurveTimeValue,CurveCompatible


def asDiscretePointCurve(curve:CurveCompatible):
    """
    Create a DiscretePointCurve from the data given.

    If it is already a DiscretePointCurve, return it.
    Otherwise, create a DiscretePointCurve
    to wrap it.
    """
    if isinstance(curve,DiscretePointCurve):
        return curve
    return DiscretePointCurve(curve)


class DiscretePointCurve(CurveBase[CurveValueT]):
    """
    A basic gaussian curve
    """
    def __init__(self,
        samples:CurveCompatible,
        interpolation:str='linear'):
        """ """
        self._samples=np.array(samples)
        self.interpolation:str=interpolation

    @property
    def start(self)->CurveValueT:
        """
        start index
        """
        return 0

    @property
    def end(self)->CurveValueT:
        """
        end index
        """
        return len(self._samples)

    def append(self,values:CurveCompatible)->None:
        """
        Append any number of values to this curve
        """
        allPointLists=[self._samples]
        def _recursiveAppend(values):
            if isinstance(values,CurveBase):
                allPointLists.extend(values.samples())
            elif hasattr(values,'__iter__'):
                for v in values:
                    _recursiveAppend(v)
            else:
                allPointLists.append((v,))
        _recursiveAppend(values)
        self._samples=np.concatenate(allPointLists)
    extend=append
    concatinate=append

    def valueAt(self,position:CurveTimeValue)->CurveValueT:
        """
        Get value at a given point
        """
        if position==int(position):
            return self._samples[position]
        x=range(len(self._samples))
        if self.interpolation=='linear':
            return np.interp(position,x,self._samples)
        return scipy.interpolate.interp1d(
            x,
            self._samples,
            kind=self.interpolation)

    def __setitem__(self,idx:CurveTimeValue,value:CurveValueT):
        if idx!=int(idx):
            raise NotImplementedError("It would be nice to set non-uniform indices, but we currently cannot do that") # noqa: E501 # pylint: disable=line-too-long
        self._samples[idx]=value

    def samples(self,
        start:typing.Optional[CurveTimeValue]=None,
        stop:typing.Optional[CurveTimeValue]=None,
        step:CurveTimeValue=1
        )->np.ndarray:
        """
        Get a block of samples
        """
        if start is None and stop is None:
            return self._samples
        return np.array(
            self.valueAt(position) for position in range(start,stop,step))
