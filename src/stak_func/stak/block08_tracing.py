from sys import _getframe, settrace
from time import time

from .block00_typing import *
from .block02_commonData import callFlag, retFlag, setFlag, delFlag
from .block03_log import appendToLog
from .block06_creatingMroCallChains import splitLinkFromFrame


def handleCall(frame, _, now=time, flag=callFlag, linker=splitLinkFromFrame):  # type: (FrameType, None, Cal[[], float], str, Cal[[FrameType], Uni[Tup[Lst[str], str], Tup[str, int, str]]]) -> None
    appendToLog((now(), flag, linker(frame)))

def handleLine(_, __):  # type: (FrameType, None) -> None
    return

def handleRet(frame, retArg, now=time, flag=retFlag, linker=splitLinkFromFrame):  # type: (FrameType, None, Cal[[], float], str, Cal[[FrameType], Uni[Tup[Lst[str], str], Tup[str, int, str]]]) -> None
    appendToLog((now(), flag, linker(frame)))

def handleExc(_, __):  # type: (FrameType, Tup[Typ[BaseException], BaseException, TracebackType]) -> None
    return

def trace(frame, event, arg, handlersByEvent={'call': handleCall, 'line': handleLine, 'return': handleRet, 'exception': handleExc}):
    # type: (FrameType, str, Any, Dic[str, Cal[[FrameType, Any], None]]) -> Cal[[FrameType, str, Any]]
    handlersByEvent[event](frame, arg)
    return trace

# The main reason to append trace entries to the main log is to keep the order, since timestamps are not precise enough for this.
# Also splitting logs before saving is very easy, another option could have been to keep a counter, but this seems simpler & faster.

def setTrace(now=time, flag=setFlag):  # type: (Cal[[], float], str) -> None
    appendToLog((now(), flag, splitLinkFromFrame(_getframe(1))))
    settrace(trace)

def delTrace(now=time, flag=delFlag):  # type: (Cal[[], float], str) -> None
    appendToLog((now(), flag, splitLinkFromFrame(_getframe(1))))
    settrace(None)
