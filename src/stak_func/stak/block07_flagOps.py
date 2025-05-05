from .block00_typing import *
from .block03_constants import defaultSegFlag

def getSegFlag(frame, segFlagName='segFlag', _defaultSegFlag=defaultSegFlag):
    globs = frame.f_globals
    if segFlagName in globs:
        return globs[segFlagName]
    return _defaultSegFlag

