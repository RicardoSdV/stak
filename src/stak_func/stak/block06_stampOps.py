from datetime import datetime

from .block00_typing import *


def tupleOfStrsToStr(strsStamp):  # type: (Str4) -> str
    return '{}:{}:{}.{}'.format(*strsStamp)

def unixStampToTupleOfStrs(stamp, dt=datetime.fromtimestamp):  # type: (float, Cal[[float], datetime]) -> Str4
    dt = dt(stamp)
    return '{:02}'.format(dt.hour), '{:02}'.format(dt.minute), '{:02}'.format(dt.second), '{:03}'.format(dt.microsecond//1000)

def unixStampToStr(unixStamp, dt=datetime.fromtimestamp):  # type: (float, Cal[[float], datetime]) -> str
    dt = dt(unixStamp)
    return '{:02}:{:02}:{:02}.{:03}'.format(dt.hour, dt.minute, dt.second, dt.microsecond//1000)


## Out of use
# def datetimeToTupleOfInts(dtStamp):  # type: (datetime) -> Int4
#     return dtStamp.hour, dtStamp.minute, dtStamp.second, dtStamp.microsecond//1000
#
# def tupleOfIntsToTupleOfStrs(intsStamp):  # type: (Int4) -> Str4
#     return (
#         '{:02}'.format(intsStamp[0]),
#         '{:02}'.format(intsStamp[1]),
#         '{:02}'.format(intsStamp[2]),
#         '{:03}'.format(intsStamp[3]),
#     )
#
# def unixStampToTupleOfInts(unixStamp):  # type: (float) -> Int4
#     dt = unixStampToDatetime(unixStamp)
#     return dt.hour, dt.minute, dt.second, dt.microsecond//1000
