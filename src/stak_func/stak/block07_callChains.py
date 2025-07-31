from types import FunctionType

from .block00_typing  import *
from .block03_constants import ignorePaths

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

    isPriv = calName[:2] == '__' and calName[-2:] != '__'
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

def makeSplitLink(
        frame,                         # type: FrameType
        dataForLogging = None,         # type: Opt[Tup[Tup[str, str], ...]]
        _ignorePaths   = ignorePaths,  # type: Set[str]
):                                     # type: (...) -> Opt[SplitLink]

    codeObj = frame.f_code
    path = codeObj.co_filename

    if path in _ignorePaths:
        return None

    calName = codeObj.co_name
    mroClsNs = tuple(iterMroUntilDefClsFound(calName, frame.f_locals, codeObj)) or None
    return path, frame.f_lineno, mroClsNs, calName, dataForLogging


def makeCallChain(
        frame,                           # type: FrameType
        firstFrameData = None,           # type: Opt[Tup[Tup[str, str], ...]]
        makeSplitLink  = makeSplitLink,  # type: Cal[[FrameType, Opt[Tup[Tup[str, str], ...]]], Opt[splitLink]]
):                                       # type: (...) -> Itrt[SplitLink]

    splitLink = makeSplitLink(frame, firstFrameData)
    if splitLink: yield splitLink
    frame = frame.f_back

    while frame:
        splitLink = makeSplitLink(frame)
        if splitLink: yield splitLink
        frame = frame.f_back

def makeCallChain2(
        frame,                        # type: FrameType
        firstFrameData=None,          # type: Opt[Tup[Tup[str, str], ...]]
        makeSplitLink=makeSplitLink,  # type: Cal[[FrameType, Opt[Tup[Tup[str, str], ...]]], Opt[splitLink]]
):                                    # type: (...) -> Lst[SplitLink]
    callChain = []; append = callChain.append

    splitLink = makeSplitLink(frame, firstFrameData)
    if splitLink: append(splitLink)
    frame = frame.f_back

    while frame:
        splitLink = makeSplitLink(frame)
        if splitLink: append(splitLink)
        frame = frame.f_back

    return callChain
