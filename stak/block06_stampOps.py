from .block00_autoImports import *

def str4ToStr(strsStamp):  # type: (Str4) -> str
    return '{}:{}:{}.{}'.format(*strsStamp)

def floatToStr4(stamp):  # type: (float) -> Str4
    dt = fromTimeStamp(stamp)
    return '{:02}'.format(dt.hour), '{:02}'.format(dt.minute), '{:02}'.format(dt.second), '{:03}'.format(dt.microsecond//1000)

def unixStampToStr(unixStamp):  # type: (float) -> str
    dt = fromTimeStamp(unixStamp)
    return '{:02}:{:02}:{:02}.{:03}'.format(dt.hour, dt.minute, dt.second, dt.microsecond//1000)
