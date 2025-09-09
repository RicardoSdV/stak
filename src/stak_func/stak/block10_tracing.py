from sys         import _getframe as getFrame, gettrace, settrace
from itertools   import izip
from time        import time

from .block00_typing     import *
from .block02_settingObj import so
from .                   import block03_constants as cs
from .block04_log        import appendToTrace
from .block05_pathOps    import getTracePath, getCompactTracePath
from .block06_stampOps   import unixStampToStr
from .block07_callChains import iterMroUntilDefClsFound
from .block08_joinLinks  import joinLink
from .block15_utils      import funcErr, listErr

setFlag , callFlag , retFlag , delFlag  = cs.traceFlags
pSetFlag, pCallFlag, pRetFlag, pDelFlag = cs.pTraceFlags

def makeSplitLinkTrace(
        frame,                             # type: FrameType
        dataForLogging   = None,           # type: Opt[Tup[Tup[str, str], ...]]
        calledFromLineno = None,           # type: int
        ignorePaths      = cs.ignorePaths, # type: Set[str]
):                                         # type: (...) -> Opt[SplitLinkTrace]

    codeObj = frame.f_code
    path = codeObj.co_filename
    if path in ignorePaths:
        return None

    calName = codeObj.co_name
    mroClsNs = tuple(iterMroUntilDefClsFound(calName, frame.f_locals, codeObj)) or None
    return path, frame.f_lineno, mroClsNs, calName, dataForLogging, calledFromLineno

def trace(
        frame,                       # type: FrameType
        event,                       # type: TraceEvent
        arg,                         # type: Any
        _now             = time,     # type: Time
        calledFromLineno = None,     # type: int
        callFlag         = callFlag, # type: str
        retFlag          = retFlag,  # type: str
):                                   # type: (...) -> 'trace'

    if event == 'call':
        flag = callFlag
        prevFrame = frame.f_back
        calledFromLineno = prevFrame.f_lineno if prevFrame else frame.f_lineno
    elif event == 'return':
        flag = retFlag
    else:
        return trace

    splitLinkTrace = makeSplitLinkTrace(frame, None, calledFromLineno)
    if not splitLinkTrace:
        return trace

    appendToTrace((_now(), flag, splitLinkTrace))
    return trace

def setTrace():
    delTrace()
    traceState.mayHave = True

    if not so.silenceTrace:
        splitLink = makeSplitLinkTrace(getFrame(1))
        if splitLink:
            appendToTrace((time(), setFlag, splitLink))
        settrace(trace)

def delTrace():
    traceState.mayHave = False

    oldTrace = gettrace()
    if oldTrace is not None:
        splitLink = makeSplitLinkTrace(getFrame(1))
        if splitLink:
            appendToTrace((time(), delFlag, splitLink))
        settrace(None)

def saveTraceLog(
        traceLog,                # type: TraceLog
        _toStr=unixStampToStr,   # type: Cal[[float], str]
        joinLink=joinLink,       # type: Cal[[SplitLink], str]
        _padByNot={noPad: pad for noPad, pad in izip(cs.traceFlags, cs.pTraceFlags)},
        callFlag=callFlag, retFlag=retFlag, setFlag=setFlag, delFlag=delFlag,
        emptyJoin = ''.join, callsJoin = ' -> '.join,
        retsJoin = ' <- '.join, space4Join = '    '.join,
        direction=None, traceFile=None, compactFile=None,
):
    if not traceLog or (not so.saveTrace and not so.saveTraceCompact):
        return

    try:
        popTrace = traceLog.popleft;

        if so.saveTrace:
            traceFile = open(getTracePath(), 'w')
            writeTrace = traceFile.write
        else:
            writeTrace = None

        if so.saveTraceCompact:
            compactFile = open(getCompactTracePath(), 'w'); writeComp = compactFile.write
            calls    = []; appCalls    = calls.append   ; popCalls = calls.pop
            callLens = []; appCallLens = callLens.append; popCallLens = callLens.pop
            rets     = []; appRets     = rets.append
            retLens  = []; appRetLens  = retLens.append
        else:
            writeComp = listErr
            calls    = listErr; appCalls    = funcErr; popCalls    = funcErr
            callLens = listErr; appCallLens = funcErr; popCallLens = funcErr
            rets     = listErr; appRets     = funcErr;
            retLens  = listErr; appRetLens  = funcErr;

        while traceLog:
            # We're running at the limits of memory, can't hold the split links and the
            # joined links at the same time.

            stamp, flag, splitLink = popTrace()
            filePath, lineno, mroClsNs, calName, data, callerLineno = splitLink

            strLink = joinLink((filePath, lineno, mroClsNs, calName, data))

            if traceFile is not None:
                writeTrace(
                    emptyJoin(
                        (_toStr(stamp), _padByNot[flag], strLink, '\n')
                    )
                )

            if compactFile is None:
                continue

            # Format and save compact trace.
            # So, the reason we can't compare bare string links is that return event frames belong to the
            # line of the function return and the call events to the line of the function definition.
            # ---------------------------------------------------------------------------------------------------------
            if flag == callFlag:
                # On direction reversal: was returning :: is calling
                # -----------------------------------------------------------------------------------------------------
                if direction == 'returning':
                    direction = 'calling'
                    retToCall = calls[-1]
                    retToCallLen = callLens[-1]
                    numSpaces = sum(callLens) - retToCallLen
                    padding = ' ' * numSpaces
                    joinedRetsAndFirstCalls = padding + retToCall + ' <- ' + retsJoin(rets) + '\n' + padding + retToCall + ' -> '
                    writeComp(joinedRetsAndFirstCalls)
                    del rets[:]
                # -----------------------------------------------------------------------------------------------------

                if callerLineno:
                    strLink = ':%s -> %s' % (callerLineno, strLink)
                else:
                    strLink = ' -> ' + strLink

                writeComp(strLink)
                appCalls(strLink)
                appCallLens(len(strLink))

            elif flag == retFlag:
                popCalls()
                popCallLens()
                appRets(strLink)
                appRetLens(len(strLink))

                # On direction reversal: was calling :: is returning
                # -----------------------------------------------------------------------------------------------------
                if direction == 'calling':
                    direction = 'returning'
                    writeComp('\n')
                # -----------------------------------------------------------------------------------------------------

            elif flag == setFlag:
                direction = 'calling'
                writeComp(strLink)
                appCallLens(len(strLink))

            elif flag == delFlag:
                direction = 'calling'
                writeComp(strLink + ' <- ' + retsJoin(rets) + '\n')
                del rets[:]

            else:
                raise ValueError('Wrong flag in traceLog, flag=%s' % flag)

# -------------------------------------------------------------------------------------------------

    finally:
        if traceFile   is not None: traceFile.close()
        if compactFile is not None: compactFile.close()


class TraceState(object):
    __slots__ = ('mayHave', )

    def __init__(self):
        # This is not weather or not a trace actually exists, it means,
        # weather or not the trace would have existed if the trace had
        # not been silenced.
        self.mayHave = False

traceState = TraceState()




# For documentation about types
#
# def handleCall(frame, _):  # type: (FrameType, None) -> None
# def handleLine(_, __):  # type: (FrameType, None) -> None
# def handleRet(frame, retArg): # type: (FrameType, None) -> None
# def handleExc(_, __):  # type: (FrameType, Tup[Typ[BaseException], BaseException, TracebackType]) -> None
