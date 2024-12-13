from datetime import datetime

from .block0_typing import *

unixStampToDatetime = datetime.fromtimestamp  # type: Cal[[float], datetime]

def datetimeToTupleOfInts(dtStamp):  # type: (datetime) -> Tup[int, int, int, int]
    return dtStamp.hour, dtStamp.minute, dtStamp.second, dtStamp.microsecond//1000

def tupleOfIntsToTupleOfStrs(intsStamp):  # type: (Tup[int, int, int, int]) -> Tup[str, str, str, str]
    return (
        '{:02}'.format(intsStamp[0]),
        '{:02}'.format(intsStamp[1]),
        '{:02}'.format(intsStamp[2]),
        '{:03}'.format(intsStamp[3]),
    )

def tupleOfStrsToStr(strsStamp):  # type: (Tup[str, str, str, str]) -> str
    return '{}:{}:{}.{}'.format(*strsStamp)

def unixStampToTupleOfInts(unixStamp):  # type: (float) -> Tup[int, int, int, int]
    dt = unixStampToDatetime(unixStamp)
    return dt.hour, dt.minute, dt.second, dt.microsecond//1000

def unixStampToTupleOfStrs(unixStamp):  # type: (float) -> Tup[str, str, str, str]
    dt = unixStampToDatetime(unixStamp)
    return '{:02}'.format(dt.hour), '{:02}'.format(dt.minute), '{:02}'.format(dt.second), '{:03}'.format(dt.microsecond//1000)

def unixStampToStr(unixStamp):  # type: (float) -> str
    dt = unixStampToDatetime(unixStamp)
    return '{:02}:{:02}:{:02}.{:03}'.format(dt.hour, dt.minute, dt.second, dt.microsecond//1000)
