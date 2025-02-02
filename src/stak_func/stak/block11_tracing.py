from sys import _getframe, settrace
from time import time

from .block00_typing import *
from .block03_commonData import callFlag, retFlag, setFlag, delFlag
from .block05_log import appendToTrace
from .block09_creatingMroCallChains import splitLinkFromFrame


def handleCall(frame, _, now=time, flag=callFlag, linker=splitLinkFromFrame, log=appendToTrace):
    # type: (FrameType, None, Time, str, Cal[[FrameType], SplitLink], App) -> None
    log((now(), flag, linker(frame)))

def handleLine(_, __):  # type: (FrameType, None) -> None
    return

def handleRet(frame, retArg, now=time, flag=retFlag, linker=splitLinkFromFrame, log=appendToTrace):
    # type: (FrameType, None, Time, str, Cal[[FrameType], SplitLink], App) -> None
    log((now(), flag, linker(frame)))

def handleExc(_, __):  # type: (FrameType, Tup[Typ[BaseException], BaseException, TracebackType]) -> None
    return

def trace(frame, event, arg, handlersByEvent={'call': handleCall, 'line': handleLine, 'return': handleRet, 'exception': handleExc}):
    # type: (FrameType, str, Any, Dic[str, Cal[[FrameType, Any], None]]) -> ...
    handlersByEvent[event](frame, arg)
    return trace

def setTrace(silence=False):
    if silence: return

    appendToTrace((time(), setFlag, splitLinkFromFrame(_getframe(1))))
    settrace(trace)

def delTrace():
    appendToTrace((time(), delFlag, splitLinkFromFrame(_getframe(1))))
    settrace(None)
