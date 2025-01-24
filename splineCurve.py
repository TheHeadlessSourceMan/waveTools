"""
A curve represented by spline points
"""
hasPyTorch=False
hasCuPy=False
try:
    # try gpu-accelerated alternatives
    import cupy as np # type: ignore
    hasCuPy=True
except ImportError:
    import numpy as np
    try:
        import torch # type: ignore
        hasPyTorch=True
    except ImportError:
        pass


def fitSplineToPoints():
    """
    Do a best-fit of spline wave to points

    See also:
    https://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html#spline-interpolation
    With discontinuities:
    https://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html#piecewise-polynomial-interpolation-splines
    """
    if hasPyTorch and not hasCuPy:
        # Define the time values and corresponding points
        t=torch.tensor([0,1,2,3,4],dtype=torch.float)
        points=torch.tensor([[0,0],[1,1],[2,0],[3,1],[4,0]],dtype=torch.float)
        # Fit a cubic spline to the points using the bspline function
        return torch.tensor.bspline(t,points,3)
    # Define the time values and corresponding points
    t=np.array([0,1,2,3,4])
    points=np.array([[0,0],[1,1],[2,0],[3,1],[4,0]])
    # Fit a cubic spline to the points using the B-spline function
    return np.poly1d(np.polyfit(t,points,3))


def evaluateSplineAtTime(spline,time):
    """
    Function to evaluate a spline-type wave at a given time
    """
    if hasPyTorch and not hasCuPy:
        time=torch.tensor(2.5,dtype=torch.float)
    return spline(time)
