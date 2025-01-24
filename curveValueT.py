"""
typing shennanigans
"""
import typing
from rangeTools.numberLike import NumberLike


CurveValueT=typing.TypeVar("CurveValueT",bound=NumberLike)
