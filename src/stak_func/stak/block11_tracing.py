import traceback
import sys
from time import time

from .block00_typing import *
from .block03_constants import callFlag, retFlag, setFlag, delFlag
from .block04_log import appendToTrace
from .block08_creatingMroCallChains import makeSplitLink


def handleCall(frame, _, now=time, flag=callFlag, linker=makeSplitLink, log=appendToTrace):
    # type: (FrameType, None, Time, str, Cal[[FrameType], SplitLink], App) -> None
    log((now(), flag, linker(frame)))

def handleLine(_, __):  # type: (FrameType, None) -> None
    return

def handleRet(frame, retArg, now=time, flag=retFlag, linker=makeSplitLink, log=appendToTrace):
    # type: (FrameType, None, Time, str, Cal[[FrameType], SplitLink], App) -> None
    log((now(), flag, linker(frame)))

def handleExc(_, __):  # type: (FrameType, Tup[Typ[BaseException], BaseException, TracebackType]) -> None
    return

def trace(frame, event, arg, handlersByEvent={'call': handleCall, 'line': handleLine, 'return': handleRet, 'exception': handleExc}):
    # type: (FrameType, TraceEvent, Any, Dic[str, Cal[[FrameType, Any], None]]) -> ...
    handlersByEvent[event](frame, arg)
    return trace

def setTrace(silence=False):
    if silence: return

    oldTrace = sys.gettrace()
    if oldTrace is not None:
        print 'ERROR: Setting a stak trace before the old one:', oldTrace
        traceback.print_stack()
        return

    appendToTrace((time(), setFlag, makeSplitLink(sys._getframe(1))))
    sys.settrace(trace)

def delTrace():
    oldTrace = sys.gettrace()
    if oldTrace is None:
        print 'ERROR: Trying to delete a trace that does not exist'
        traceback.print_stack()
        return

    appendToTrace((time(), delFlag, makeSplitLink(sys._getframe(1))))
    sys.settrace(trace)
