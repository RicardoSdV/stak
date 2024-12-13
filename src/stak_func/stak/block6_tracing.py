from time import time

from .block1_commonData import *
from .block3_stampOps import *
from .block4_creatingMroCallChains import *


def __call__(frame, event, arg):  # type: (FrameType, str, Any) -> 'STAK'
    """ Used only to set an instance of STAK as a trace """

    if event == 'call' or event == 'return':
        traceEntry(event, frame)
    elif event == 'line' or event == 'exception':
        pass
    else:
        print 'ERROR: from STAK.__call__ unforeseen event string: {}'.format(event)

    return

def traceEntry(flag, frame):  # type: (FrameType, str) -> None
    # All entries to trace log made through this method
    appendToTraceLog(
        (time(), flag, splitLinkFromFrame(frame))
    )

traceOriginatorEntry = partial(traceEntry, 'originator')
traceTerminatorEntry = partial(traceEntry, 'terminator')

def prodCallTreeUntilReset():  # type: () -> Gen[None, Tup[float, str, str], Lst[Uni[int, str]]]
    # Trace func is set, & it produces a set of log entries which reproduce the entire call tree.
    # Then trace func is removed. More trace funcs could be set, & all their output is appended to the
    # same traceLog. So, this, produces the call branches from the log entries.


    oldTime, flag, jointLink = (yield)
    newTime = oldTime
    depth = 0
    callChain = [unixStampToStr(oldTime), traceFlag]

    while flag == 'call':
        if oldTime != newTime:
            callChain.append('<{}>{}'.format(int((newTime - oldTime) * 1000), jointLink))
            oldTime = newTime
        else:
            callChain.append(jointLink)
        depth += 1

        newTime, flag, jointLink = (yield)

    oldTime = newTime
    returnChain = [unixStampToStr(oldTime), traceFlag]

    while flag == 'return':
        pass

def formatTraceLog(traceLog):  # type: () -> Itrt[str]

    # Receives the raw trace log, sends all the elements into the joiner, it joins one set of call entries &
    # one set of return entries, returning them as two log lines using the StopIteration exception.
    # Also in the return comes the final depth, which is used to start the next two lines at the right indent.
    # Once the joiner is exhausted it creates a new one, to handle the next two lines, and so on.

    _callableNames = callableNames
    joiner = prodCallTreeUntilReset(); joiner.next()
    for unixStamp, flag, splitLink in traceLog:
        if splitLink[-1] in callableNames:
            continue  # If tracing any of STAKS' callables skip that

        try:
            joiner.send((unixStamp, flag, splitLink))
        except StopIteration as exc:
            callLine, returnLine, finalDepth = exc.message
