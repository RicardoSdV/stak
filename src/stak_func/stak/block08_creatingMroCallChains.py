from sys import _getframe
from time import time
from types import FunctionType

from .block00_typing import *
from .block04_log import appendToLog

# For some reason instance methods are FunctionType, at runtime, but not when testing
# them out in the console, so isinstance(method, MethodType) is False at runtime, but
# True in the console, so, yeah, what's going on there?

def iterMroUntilDefClsFound(calName, fLocals, codeObjToFindDefClsOf):
    if 'self' in fLocals:
        callerCls = fLocals['self'].__class__
        isIns = True
    elif 'cls' in fLocals:
        callerCls = fLocals['cls']
        isIns = False
    else:
        return

    if not isinstance(callerCls, type): return  # Old style classes not supported

    isPriv = calName.startswith('__') and not calName.endswith('__')
    for cls in callerCls.__mro__:
        yield cls.__name__

        mangledMaybeName = '_' + cls.__name__.rstrip('_') + calName if isPriv else calName
        if mangledMaybeName not in cls.__dict__:
            continue

        clsAttr = cls.__dict__[mangledMaybeName]
        if isinstance(clsAttr, property):
            if getattr(clsAttr.fget, '__code__', None) is codeObjToFindDefClsOf: return
            if getattr(clsAttr.fset, '__code__', None) is codeObjToFindDefClsOf: return
            if getattr(clsAttr.fdel, '__code__', None) is codeObjToFindDefClsOf: return
            continue

        if isIns:
            if isinstance(clsAttr, FunctionType) and clsAttr.__code__ is codeObjToFindDefClsOf:
                return
        else:
            if isinstance(clsAttr, classmethod) and clsAttr.__func__.__code__ is codeObjToFindDefClsOf:
                return

def makeSplitLink(frame, dataForLogging=None):  # type: (FrameType, Opt[Tup[Tup[str, str], ...]]) -> SplitLink
    codeObj = frame.f_code
    calName = codeObj.co_name
    mroClsNs = tuple(iterMroUntilDefClsFound(calName, frame.f_locals, codeObj)) or None
    return codeObj.co_filename, frame.f_lineno, mroClsNs, calName, dataForLogging

def makeCallChain(frame, firstFrameData=None):  # type: (FrameType, Opt[Tup[Tup[str, str], ...]]) -> Itrt[SplitLink]
    yield makeSplitLink(frame, firstFrameData)
    frame = frame.f_back

    while frame:
        yield makeSplitLink(frame)
        frame = frame.f_back

def omrolocs(log=appendToLog, now=time, frame=_getframe, callChain=makeCallChain):  # type: (App, Time, GF, Cal[[FrameType], Itrt[SplitLink]]) -> None
    """ Optional Method Resolution Order Logger Optional Call Stack """
    log((now(), tuple(callChain(frame(1)))))
