"""
I have a better version somewhere
"""

PercentCompatible=float

def asPercent(percent:PercentCompatible):
    """
    Convert to percent
    """
    if isinstance(percent,Percent):
        return percent
    return Percent(percent)

class Percent(float):
    """
    Special case of a float
    """
    def __repr__(self):
        return f'{float.__repr__(self)*100}%'
