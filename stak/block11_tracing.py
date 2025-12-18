from .block00_autoImports import *

setFlag , callFlag , retFlag , delFlag  = traceFlags
pSetFlag, pCallFlag, pRetFlag, pDelFlag = pTraceFlags

_traceLinkWithLnBFs = pathBF | linenoBF | calNameBF | callFromLnBF

def trace(
        frame,                                         # type: FrameType
        event,                                         # type: TraceEvent
        arg,                                           # type: Any
        _clock = clock,                                # type: Clock
        _traceEntryBFs = strFlagBF | stampBF | linkBF, # type: int
):                                                     # type: (...) -> 'trace'

    if event == 'call':
        flag = callFlag
        prevFrame = frame.f_back
        if prevFrame:
            splitLink = makeSplitLink(frame, None, _traceLinkWithLnBFs, extras=[prevFrame.f_lineno])
        else:
            splitLink = makeSplitLink(frame)
    elif event == 'return':
        flag = retFlag
        splitLink = makeSplitLink(frame)
    else:
        return trace

    if not splitLink:
        return trace

    if printLiveTrace:
        print 'STAK: TRACE:', flag, joinLink(splitLink)

    traceLogExt((_traceEntryBFs, flag, _clock()))
    traceLogExt(splitLink)
    return trace

def setTrace():
    delTrace()
    traceState.mayHave = True

    if not silenceTrace:
        splitLink = makeSplitLink(sysGetFrame(1))
        if splitLink:
            appendToTrace((time(), setFlag, splitLink))
        sysSetTrace(trace)

def delTrace():
    traceState.mayHave = False

    oldTrace = sysGetTrace()
    if oldTrace is not None:
        splitLink = makeSplitLinkTrace(sysGetFrame(1))
        if splitLink:
            appendToTrace((time(), delFlag, splitLink))
        sysSetTrace(None)


def saveTraceLog(
        traceLog,                # type: TraceLog
        _padByNot={noPad: pad for noPad, pad in izip(traceFlags, pTraceFlags)},
        emptyJoin = ''.join, callsJoin = ' -> '.join,
        retsJoin = ' <- '.join, space4Join = '    '.join,
        direction=None, traceFile=None, compactFile=None,
):
    if not traceLog or (not saveTrace and not saveTraceCompact):
        return

    try:
        popTrace = traceLog.popleft;

        if saveTrace:
            traceFile = open(getTracePath(), 'w')
            writeTrace = traceFile.write
        else:
            writeTrace = None

        if saveTraceCompact:
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
                        (unixStampToStr(stamp), _padByNot[flag], strLink, '\n')
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


def onSettingsReload_updateTracing(oldSettings, newSettings):
    if not traceState.mayHave:
        return

    wasSilenced = oldSettings['silenceTrace']
    isSilenced = newSettings['silenceTrace']

    if wasSilenced == isSilenced:
        return

    if isSilenced:
        delTrace()
    else:
        setTrace()


# For documentation about types
#
# def handleCall(frame, _):  # type: (FrameType, None) -> None
# def handleLine(_, __):  # type: (FrameType, None) -> None
# def handleRet(frame, retArg): # type: (FrameType, None) -> None
# def handleExc(_, __):  # type: (FrameType, Tup[Typ[BaseException], BaseException, TracebackType]) -> None
