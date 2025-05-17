import sys
from time import time

from .block00_typing import *
from .block02_settingObj import so
from .block03_constants import callFlag, retFlag, setFlag, delFlag
from .block04_log import appendToTrace
from .block07_creatingMroCallChains import makeSplitLink
from .z_utils import E


def trace(frame, event, arg):  # type: (FrameType, TraceEvent, Any) -> ...
    if event == 'call':
        splitLink = makeSplitLink(frame)
        if splitLink: appendToTrace((time(), callFlag, splitLink))

    elif event == 'return':
        splitLink = makeSplitLink(frame)
        if splitLink: appendToTrace((time(), retFlag, splitLink))

    return trace

def setTrace():
    traceState.mayHave = True
    if so.silenceTrace: return

    oldTrace = sys.gettrace()
    if oldTrace is not None:
        E('Setting a stak trace before removing the old one:', oldTrace=oldTrace)
        return

    splitLink = makeSplitLink(sys._getframe(1))
    if splitLink: appendToTrace((time(), setFlag, splitLink))
    sys.settrace(trace)

def delTrace():
    traceState.mayHave = False

    oldTrace = sys.gettrace()
    if oldTrace is None:
        E('Trying to delete a trace that does not exist')
        return

    splitLink = makeSplitLink(sys._getframe(1))
    if splitLink: appendToTrace((time(), delFlag, splitLink))
    sys.settrace(trace)


class TraceState(object): __slots__ = ('mayHave', )
traceState = TraceState()
traceState.mayHave = False

















# For documentation about types
#
# def handleCall(frame, _, now=time, flag=callFlag, linker=makeSplitLink, log=appendToTrace):
#     # type: (FrameType, None, Time, str, Cal[[FrameType], SplitLink], App) -> None
#
# def handleLine(_, __):  # type: (FrameType, None) -> None
#
# def handleRet(frame, retArg, now=time, flag=retFlag, linker=makeSplitLink, log=appendToTrace):
#     # type: (FrameType, None, Time, str, Cal[[FrameType], SplitLink], App) -> None
#
# def handleExc(_, __):  # type: (FrameType, Tup[Typ[BaseException], BaseException, TracebackType]) -> None
