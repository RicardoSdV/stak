from functools import partial

from .block00_typing import *
from .block02_commonData import *
from .block03_log import log
from .block04_pathOps import makeDirPaths, genPrimiStakPaths, genPrimiStdPaths, genCompStakPaths, genStdStakSplicePaths, genCompStdStakSplicePaths, genTracePaths, genCompactTracePaths
from .block05_stampOps import tupleOfStrsToStr, unixStampToTupleOfStrs, unixStampToStr
from .block06_creatingMroCallChains import pathSplitChar, joinFileLink, joinMroLink
from .block09_compression import compressLines

# In general the working theory is that we don't care too much about performance when saving logs, if in exchange
# performance is gained when generating, because generation takes place during critical parts of the program
# whereas saving is normally done during idle periods. This explains some of the wierd decisions.


def fmtOmrolocsEntry(stamp, theRest, toStr=tupleOfStrsToStr, flag=pOmrolocsFlag):  # type: (Str4, str, Cal[[Str4], str], str) -> str
    return toStr(stamp) + flag + ' <- '.join(theRest)

def fmtDataEntry(stamp, theRest, toStr=tupleOfStrsToStr, flag=pDataFlag):  # type: (Str4, str, Cal[[Str4], str], str) -> str
    return toStr(stamp) + flag + theRest

def fmtLabelEntry(_, theRest):  # type: (Str4, str) -> str
    return theRest

def fmtDateEntry(stamp, theRest, toStr=tupleOfStrsToStr, flag=pDateFlag):  # type: (Str4, str, Cal[[Str4], str], str) -> str
    return toStr(stamp) + flag + theRest

def formatPrimiStak(fullStrLinkCallChains, formattersByFlag={omrolocsFlag: fmtOmrolocsEntry, dataFlag: fmtDataEntry, labelFlag: fmtLabelEntry, dateFlag: fmtDateEntry}):
    # type: (Tup[Tup[Str4, str, Uni[str, Lst[str]]], ...], Dic[str, Cal[[Str4, str], str]]) -> Itrt[str]
    for stamp, flag, theRest in fullStrLinkCallChains:
        yield formattersByFlag[flag](stamp, theRest)

def formatPrimiStd(parsedStdLog, toStr=tupleOfStrsToStr, pFlags=pStdFlagsByStdFlags):
    # type: (Seq[Tup[Str4, str, str]], Cal[[Str4], str], Dic[str, str]) -> Itrt[str]
    for midStamp, stdFlag, theRest in parsedStdLog:
        yield toStr(midStamp) + pFlags[stdFlag] + theRest

def formatCompStak(callChainsWithCompressedStrLinks):  # type: (Tup[Tup[Str4, str, str], ...]) -> Lst[str]
    return compressLines(
        [entry[-1] for entry in callChainsWithCompressedStrLinks]
    )

def formatStdStakSplice(splicedLog, toStr=tupleOfStrsToStr):
    # type: (Lst[Lst[Tup[Str4, str, str]]], Cal[[Str4], str]) -> Itrt[str]
    for stamp, pFlag, theRest in splicedLog:
        yield toStr(stamp) + pFlag + theRest

def formatCompStdStakSplice(compressedStakSplice):  # type: (Lst[str]) -> Lst[str]
    return compressLines([el[-1] for el in compressedStakSplice])


def joinSplitLink(splitLink):  # type: (Uni[Tup[str, int, str], Tup[Lst[str], str]]) -> str
    if len(splitLink) == 3:
        return joinFileLink(*splitLink)
    return joinMroLink(*splitLink)

def fmtSetEntry(stamp, splitLink, toStr=unixStampToStr, flag=pSetFlag, join=joinSplitLink):
    # type: (float, Uni[Tup[str, int, str], Tup[Lst[str], str]], Cal[[float], str], str, Cal[[Uni[Tup[str, int, str], Tup[Lst[str], str]]], str]) -> str
    return toStr(stamp) + flag + join(splitLink)

def fmtCallEntry(stamp, splitLink, toStr=unixStampToStr, flag=pCallFlag, join=joinSplitLink):
    # type: (float, Uni[Tup[str, int, str], Tup[Lst[str], str]], Cal[[float], str], str, Cal[[Uni[Tup[str, int, str], Tup[Lst[str], str]]], str]) -> str
    return toStr(stamp) + flag + join(splitLink)

def fmtRetEntry(stamp, splitLink, toStr=unixStampToStr, flag=pRetFlag, join=joinSplitLink):
    # type: (float, Uni[Tup[str, int, str], Tup[Lst[str], str]], Cal[[float], str], str, Cal[[Uni[Tup[str, int, str], Tup[Lst[str], str]]], str]) -> str
    return toStr(stamp) + flag + join(splitLink)

def fmtDelEntry(stamp, splitLink, toStr=unixStampToStr, flag=pDelFlag, join=joinSplitLink):
    # type: (float, Uni[Tup[str, int, str], Tup[Lst[str], str]], Cal[[float], str], str, Cal[[Uni[Tup[str, int, str], Tup[Lst[str], str]]], str]) -> str
    return toStr(stamp) + flag + join(splitLink)

def formatTrace(traceEntries, formattersByFlag={setFlag: fmtSetEntry, callFlag: fmtCallEntry, retFlag: fmtRetEntry, delFlag: fmtDelEntry}):
    for stamp, flag, theRest in traceEntries:
        yield formattersByFlag[flag](stamp, theRest)

def formatCompactTrace(entries): return entries

def writeLogsToFile(pathGen, formatter, *logs):  # type: (Itrt[str], Cal[[Itrb], Opt[Itrb[str]]], Itrb) -> None
    for _log in logs:

        with open(next(pathGen), 'w') as _file:
            formattedLines = formatter(_log)
            if formattedLines:
                _file.writelines((
                    line + '\n' for line in formattedLines
                ))

savePrimiStak         = partial(writeLogsToFile, genPrimiStakPaths        , formatPrimiStak)
savePrimiStd          = partial(writeLogsToFile, genPrimiStdPaths         , formatPrimiStd)
saveCompStak          = partial(writeLogsToFile, genCompStakPaths         , formatCompStak)
saveStdStakSplice     = partial(writeLogsToFile, genStdStakSplicePaths    , formatStdStakSplice)
saveCompStdStakSplice = partial(writeLogsToFile, genCompStdStakSplicePaths, formatCompStdStakSplice)
saveTrace             = partial(writeLogsToFile, genTracePaths            , formatTrace)
saveCompactTrace      = partial(writeLogsToFile, genCompactTracePaths     , formatCompactTrace)

def trimFilePathAddLineno(link, splitChar=pathSplitChar):  # type: (Uni[Tup[str, int, str], Tup[Lst[str], str]], str) -> Uni[Tup[str, str], Tup[Lst[str], str]]
    # Trims path to its last two elements, adds lineno to it, yields this plus the method name
    if len(link) == 2:  # If len is 2 its an mro link
        yield link
    else:
        filePath, lineno, methName = link
        splitPath = filePath.split(splitChar)
        yield (
            '{}{}{}{}.'.format(
                splitPath[-2],
                splitChar,
                splitPath[-1].rstrip('py'),
                lineno
            ),
            methName
        )

def trimFilePathsAddLineNums(callChain, trimmer=trimFilePathAddLineno):
    # type: (Tup[Uni[Tup[str, int, str], Tup[Lst[str], str]], ...], Cal) -> Tup[Uni[Tup[str, str], Tup[Lst[str], str]], ...]
    for link in callChain:
        yield trimmer(link)

def mroLinkToStrLink(mroClsNs, methName):  # type: (Lst[str], str) -> str
    mroClsNs[-1] = '{}.{}{}'.format(mroClsNs[-1], methName, ')' * (len(mroClsNs) - 1))
    return '('.join(mroClsNs)

def preProcess(stakLog, _omrolocsFlag=omrolocsFlag, toStr=unixStampToTupleOfStrs):
    # type: (Lst[Tup[float, str, Uni[Tup[Uni[Tup[str, int, str], Tup[Lst[str], str]], ...]]]], str, Cal[[float], Str4]) -> Itrt[Tup[float, str, Uni[str, Tup[Uni[Tup[str, str], Tup[Lst[str], str]], ...]]], ...]
    """ Turn the unix stamps to tuples of strs, trim file path to the last two elements, add lineno to it. """

    for unixStamp, flag, theRest in stakLog:
        yield (
            toStr(unixStamp),
            flag,
            tuple(trimFilePathsAddLineNums(theRest)) if flag == _omrolocsFlag else theRest
        )

def entriesWithLinksJoin(preProcStakLog, _omrolocsFlag=omrolocsFlag, linker=mroLinkToStrLink):
    # type: (Itrt[Tup[float, str, Uni[str, Tup[Uni[Tup[str, str], Tup[Lst[str], str]], ...]]], ...], str, Cal[[Lst[str], str], str]) -> Itrt[Tup[Str4, str, Uni[str, Tup[str, ...]]]]

    for stamp, flag, theRest in preProcStakLog:
        if flag == _omrolocsFlag:
            yield stamp, flag, tuple((  # At this point theRest is the splitLinkCallChain
                bigNameSpace + methName if isinstance(bigNameSpace, str)
                else linker(bigNameSpace[:], methName)
                for bigNameSpace, methName in theRest
            ))
        else:
            yield stamp, flag, theRest

def spliceStakLogWithStdLog(stdLog, stakLog):
    # type: (Tup[Tup[Str4, str, str], ...], Tup[Tup[Str4, str, str], ...]) -> Itrt[Tup[Str4, str, str]]

    stdIdx, stakIdx = 0, 0
    stdElLeft, stakElLeft = True, True
    lenStd, lenStak = len(stdLog), len(stakLog)

    stdStamp, stdFlag, stdTheRest = stdLog[stdIdx]
    stamp   , flag   , theRest    = stakLog[stakIdx]

    while stdElLeft or stakElLeft:

        if stdElLeft is True and (stdStamp <= stamp or stakElLeft is False):
            yield stdStamp, allPflagsByFlags[stdFlag], stdTheRest
            stdIdx += 1
            if stdIdx == lenStd:
                stdElLeft = False
            else:
                newStamp, stdFlag, stdTheRest = stdLog[stdIdx]
                if newStamp is not None:
                    stdStamp = newStamp

        if stakElLeft is True and (stdStamp > stamp or stdElLeft is False):
            yield stamp, allPflagsByFlags[flag], theRest
            stakIdx += 1
            if stakIdx == lenStak:
                stakElLeft = False
            else:
                stamp, flag, theRest = stakLog[stakIdx]

def stdStakSplice(stdLogs, stakLog):
    # type: (Tup[Tup[Tup[Str4, str, str], ...], ...], Tup[Tup[Str4, str, str], ...]) -> Lst[Lst[Tup[Str4, str, str]]]
    return [
        list(spliceStakLogWithStdLog(stdLog, stakLog))
        for stdLog in stdLogs
    ]

def splitLog(_traceFlags=traceFlags):  # type: (Set[str]) -> ...
    traceLog, stakLog = [], []; traceApp, stakApp = traceLog.append, stakLog.append

    for entry in log:  # type: Tup[float, str, Uni[Tup[Uni[Tup[str, int, str], Tup[Lst[str], str]], ...]]]
        if entry[1] in _traceFlags:
            traceApp(entry)
        else:
            stakApp(entry)

    return traceLog, stakLog

def removeStakCallables(traceLog, calNames=callableNames):
    # type: (Lst[Tup[float, str, Uni[Tup[str, int, str], Tup[Lst[str], str]]]], Set[str]) -> Itrt[Tup[float, str, Uni[Tup[str, int, str], Tup[Lst[str], str]]]]
    for entry in traceLog:
        if entry[-1][-1] not in calNames:
            yield entry

def makeOpenCalls(openCalls, _callFlags=callFlags, _retFlags=retFlags):
    # type: (Itrt[Tup[float, str, Uni[Tup[str, int, str], Tup[Lst[str], str]]]], Set[str], Set[str]) -> Itrt[Lst[Uni[Tup[str, int, str], Tup[Lst[str], str]]]]
    calls = []
    appCalls = calls.append
    popCalls = calls.pop

    for stamp, flag, link in openCalls:
        if flag in _callFlags:
            appCalls(link)
        elif flag in _retFlags:
            retLink = popCalls()
            assert retLink[0] == link[0]
            assert retLink[-1] == link[-1]
        else:
            raise NotImplementedError()

        yield calls[:]

def joinTraceLinks(openCalls):  # type: (Itrt[Lst[Uni[Tup[str, int, str], Tup[Lst[str], str]]]]) -> Itrt[Lst[str]]
    for links in openCalls:
        yield list(
            joinFileLink(*link) if len(link) == 3
            else joinMroLink(*link)
            for link in links
        )

def makeMinMaxOpen(openCalls):  # type: (Itrt[Lst[str]]) -> Itrt[Lst[str]]
    prevLen   = 0
    prevDir   = 'call'
    prevCalls = []
    yield prevCalls

    for calls in openCalls:
        lenCalls = len(calls)
        currDir = 'call' if lenCalls > prevLen else 'ret'

        if currDir != prevDir:
            yield prevCalls

        prevCalls = calls
        prevLen   = lenCalls
        prevDir   = currDir

    yield calls

def replaceRedundantWithSpacesInPlace(calls, num, extra='' if pathSplitChar == '/' else ' '):  # type: (Lst[str], int, str) -> None
    num = max(0, num-1)
    for i, call in enumerate(calls):
        if i < num:
            calls[i] = extra + (' ' * len(call))
        else:
            return

def makeMinMaxDiffOld(minMaxOpen):  # type: (Itrt[Lst[str]]) -> Itrt[Lst[str]]
    isCallDiff = True
    prevCalls = next(minMaxOpen)
    for calls in minMaxOpen:
        if isCallDiff:
            replaceRedundantWithSpacesInPlace(calls, len(prevCalls))
            yield calls
        else:
            replaceRedundantWithSpacesInPlace(prevCalls, len(calls))
            yield prevCalls

        isCallDiff = not isCallDiff
        prevCalls = calls

def diffAndRedundant(small, big):  # type: (Lst[str], Lst[str]) -> Itrt[Uni[str, int]]
    lastLinkInOld = small[-1] if len(small) != 0 else None
    isRedundant = True

    for el in big:
        if el == lastLinkInOld or lastLinkInOld is None:
            isRedundant = False

        if isRedundant:
            yield len(el)
        else:
            yield el

def makeMinMaxDiff(minMaxOpen):  # type: (Itrt[Lst[str]]) -> Itrt[Lst[Uni[str, int]]]
    isCallDiff = True
    prevLinks = next(minMaxOpen)
    for links in minMaxOpen:

        if isCallDiff:
            yield list(diffAndRedundant(prevLinks, links))
        else:
            yield list(diffAndRedundant(links, prevLinks))

        isCallDiff = not isCallDiff
        prevLinks = links

def splitIntsFromStrs(iterable):  # type: (Itrb[Uni[str, int]]) -> Tup[Lst[str], Lst[int]]
    strs, ints = [], []
    appStrs, appInts = strs.append, ints.append

    for el in iterable:
        if isinstance(el, str):
            appStrs(el)
        elif isinstance(el, int):
            appInts(el)
        else:
            raise ValueError()

    return strs, ints

def joinEventGroups(minMaxDiff):  # type: (Itrt[Lst[Uni[str, int]]]) -> Itrt[str]
    isCalling = True

    for diff in minMaxDiff:
        strLinks, spaceNums = splitIntsFromStrs(diff)
        joinedLinks = ' -> '.join(strLinks) if isCalling else ' <- '.join(strLinks)
        yield (' ' * sum(spaceNums)) + ('    ' * (max(0, len(spaceNums)))) + joinedLinks
        isCalling = not isCalling

def saveAll():
    makeDirPaths()

    traceLog, stakLog = splitLog()  # type: Lst[Tup[float, str, Uni[Tup[str, int, str], Tup[Lst[str], str]]]], Lst[Tup[float, str, Tup[Uni[Tup[str, int, str], Tup[Lst[str], str]], ...]]]

    # preProcessedStakLog = preProcess(stakLog)
    # strLinkStakLog = tuple(entriesWithLinksJoin(preProcessedStakLog))
    #
    # savePrimiStak(strLinkStakLog)
    #
    # callChainsWithCompressedStrLinks = tuple(compressLinks(strLinkStakLog))
    # saveCompStak(callChainsWithCompressedStrLinks)
    #
    # # Flags not padded yet
    # parsedStdLogs = tuple(parseStdLogs())  # type: Tup[Tup[Tup[Str4, str, str], ...], ...]
    #
    # savePrimiStd(*parsedStdLogs)
    #
    # splicedLogs = stdStakSplice(parsedStdLogs, callChainsWithCompressedStrLinks)
    #
    # saveStdStakSplice(*splicedLogs)
    #
    # saveCompStdStakSplice(*splicedLogs)

    # Trace
    trimTrace = removeStakCallables(traceLog)
    openCalls = makeOpenCalls(trimTrace)
    joinedOpenCalls = joinTraceLinks(openCalls)
    minMaxOpen = makeMinMaxOpen(joinedOpenCalls)
    minMaxDiff = makeMinMaxDiff(minMaxOpen)
    joinedEventGroups = joinEventGroups(minMaxDiff)

    saveCompactTrace(joinedEventGroups)

## Out of service: The idea was that sometimes the entire MRO would be unnecessary,
# but it seems that most classes don't have an inheritance chain big enough to be a problem
# def partStrLinkCreator(mroClsNs, methName):  # type: (Lst[str], str) -> str
#     return mroClsNs[-1] + methName
