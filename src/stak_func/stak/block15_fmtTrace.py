from .block00_typing import *
from .block02_commonData import callableNames, callFlags, retFlags
from .block04_log import traceLog
from .block05_pathOps import pathSplitChar
from .block07_creatingMroCallChains import joinFileLink, joinMroLink

def removeStakCallables(traceLog, calNames=callableNames):
    # type: (Lst[Tup[float, str, SplitLink]], Set[str]) -> Itrt[Tup[float, str, SplitLink]]
    for entry in traceLog:
        if entry[-1][-1] not in calNames:
            yield entry

def makeOpenCalls(openCalls, _callFlags=callFlags, _retFlags=retFlags):
    # type: (Itrt[Tup[float, str, SplitLink]], Set[str], Set[str]) -> Itrt[Lst[Uni[Tup[str, int, str], Tup[Lst[str], str]]]]
    calls = []
    appCalls = calls.append
    popCalls = calls.pop

    for stamp, flag, link in openCalls:
        if flag in _callFlags:
            appCalls(link)
        elif flag in _retFlags:
            retLink = popCalls()
            assert retLink[0] == link[0] and retLink[-1] == link[-1]
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


def formatTraceLog():  # type: () -> Itrt[str]
    trimTrace = removeStakCallables(traceLog)
    openCalls = makeOpenCalls(trimTrace)
    joinedOpenCalls = joinTraceLinks(openCalls)
    minMaxOpen = makeMinMaxOpen(joinedOpenCalls)
    minMaxDiff = makeMinMaxDiff(minMaxOpen)
    joinedEventGroups = joinEventGroups(minMaxDiff)
    return joinedEventGroups


