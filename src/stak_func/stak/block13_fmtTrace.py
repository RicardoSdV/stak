from .block00_typing import *
from .block03_constants import callFlags, retFlags
from .block05_pathOps import pathSplitChar
from .block08_joinSplitLinks import joinLink

# TODO: Yeah this is an initial implementation, all these functions should be one
#  and its not really been tested other than with the tester.py.


def makeOpenCalls(
        openCalls,             # type: Itrb[Tup[float, str, SplitLink]]
        _joinLink=joinLink,    # type: Cal[[SplitLink], str]
        _callFlags=callFlags,  # type: Set[str]
        _retFlags=retFlags,    # type: Set[str]
):                             # type: (...) -> Itrt[Lst[str]]
    calls = []; append = calls.append; pop = calls.pop

    for stamp, flag, link in openCalls:
        if flag in _callFlags:
            append(_joinLink(link))
        elif flag in _retFlags:
            pop()
        else:
            raise NotImplementedError()

        yield calls[:]

def makeMinMaxOpen(openCalls):  # type: (Itrb[Lst[str]]) -> Itrt[Lst[str]]
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

def replaceRedundantWithSpacesInPlace(
        calls,                                     # type: Lst[str]
        num,                                       # type: int
        extra='' if pathSplitChar == '/' else ' '  # type: str
):                                                 # type: (...) -> None
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
        _class = el.__class__
        if _class is str:
            appStrs(el)
        elif _class is int:
            appInts(el)
        else:
            raise ValueError()

    return strs, ints

def joinEventGroups(minMaxDiff):  # type: (Itrt[Lst[Uni[str, int]]]) -> Itrt[str]
    isCalling = True

    for diff in minMaxDiff:
        strLinks, spaceNums = splitIntsFromStrs(diff)
        joinedLinks = ' -> '.join(strLinks) if isCalling else ' <- '.join(strLinks)
        yield (' ' * sum(spaceNums)) + ('    ' * (max(0, len(spaceNums)))) + joinedLinks + '\n'
        isCalling = not isCalling


def compactTraceLog(traceLog):  # type: (TraceLog) -> Itrt[str]

    openCalls = makeOpenCalls(traceLog)
    minMaxOpen = makeMinMaxOpen(openCalls)
    minMaxDiff = makeMinMaxDiff(minMaxOpen)
    joinedEventGroups = joinEventGroups(minMaxDiff)

    return joinedEventGroups































# Deprecated in favour of one joiner in block09_joinFileLinks
# def joinTraceLinks(openCalls):  # type: (Itrt[Lst[Uni[Tup[str, int, str], Tup[Lst[str], str]]]]) -> Itrt[Lst[str]]
#     for links in openCalls:
#         yield list(
#             joinFileLink(*link) if len(link) == 3
#             else joinMroLink(*link)
#             for link in links
#         )


# Deprecated in favour of ignoring paths on log gather.
# def removeStakCallables(traceLog, calNames=callableNames):
#     # type: (Lst[Tup[float, str, SplitLink]], Set[str]) -> Itrt[Tup[float, str, SplitLink]]
#     for entry in traceLog:
#         if entry[-1][-1] not in calNames:
#             yield entry


