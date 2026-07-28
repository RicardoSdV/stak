from ..lib import dtFromTimeStamp

str4ToStr = '{}:{}:{}.{}'.format

def floatToStr4(stamp):
    dt = dtFromTimeStamp(stamp)
    return '{:02}'.format(dt.hour), '{:02}'.format(dt.minute), '{:02}'.format(dt.second), '{:03}'.format(dt.microsecond//1000)

def unixStampToStr(unixStamp):
    dt = dtFromTimeStamp(unixStamp)
    return '{:02}:{:02}:{:02}.{:03}'.format(dt.hour, dt.minute, dt.second, dt.microsecond//1000)

def absStampToDateStr(unixStamp):
    return dtFromTimeStamp(unixStamp).strftime('%Y-%m-%d')
