from itertools import izip

from .block00_typing import *
from .block02_settingObj import so
from .block03_constants import omrolocsFlag, allPflagsByFlags
from .block06_stampOps import unixStampToTupleOfStrs
from .block09_joinSplitLinks import joinLinks


# Seg flags approach is deprecated, but might pad first frame file paths in the same way
#
# def padSegFlags(stakLog, pSegFlagsBySegFlags={}):
#     # type: (Log[Tup[float, str, str, SplitLink]], Dic[str, str]) -> Dic[str, str]
#     if not pSegFlagsBySegFlags:
#         segFlags = list(set(entry[1] for entry in stakLog))
#         paddedFlags = padFlags(segFlags)
#         for segFlag, pSegFlag in izip(segFlags, paddedFlags):
#             pSegFlagsBySegFlags[segFlag] = pSegFlag
#
#     return pSegFlagsBySegFlags


def fmtStakLog(stakLog):  # type: (StakLog) -> ...
    for stamp, splitLink in stakLog:
        pass


def entriesWithLinksJoin(stakLog, hasSplitLink=omrolocsFlag, join=joinLinks, toStr=unixStampToTupleOfStrs):
    silenced = so.silencedFiles

    for stamp, segFlag, callerFlag, theRest in stakLog:
        firstFrameLink = theRest[0]
        firstFrameFilePath = firstFrameLink[0]
        if firstFrameFilePath in silenced and silenced[firstFrameFilePath]:
            continue

        if callerFlag == hasSplitLink:
            yield toStr(stamp), ': placeholder', callerFlag, tuple(join(theRest))
        else:
            yield toStr(stamp), ': placeholder', callerFlag, theRest


def spliceStakLogWithStdLog(stdLog, stakLog):
    # type: (Tup[Tup[Str4, str, str], ...], Tup[Tup[Str4, str], ...]) -> Itrt[Tup[Str4, str, str]]

    stdIdx, stakIdx = 0, 0
    stdElLeft, stakElLeft = True, True
    lenStd, lenStak = len(stdLog), len(stakLog)

    stdStamp, stdFlag, stdTheRest = stdLog[stdIdx]
    stamp, theRest = stakLog[stakIdx]

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
            yield stamp, '', theRest  # todo: stak flags
            stakIdx += 1
            if stakIdx == lenStak:
                stakElLeft = False
            else:
                stamp, theRest = stakLog[stakIdx]

def stdStakSplice(stdLogs, stakLog):
    # type: (Tup[Tup[Tup[Str4, str, str], ...], ...], Tup[Tup[Str4, str], ...], ...) -> Lst[Lst[Tup[Str4, str, str]]]
    return [
        list(spliceStakLogWithStdLog(stdLog, stakLog))
        for stdLog in stdLogs
    ]
