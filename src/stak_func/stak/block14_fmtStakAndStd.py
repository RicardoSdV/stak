from itertools import izip

from .block00_typing import *
from .block01_settings import stdLogPrefixes
from .block02_commonData import omrolocsFlag, allPflagsByFlags
from .block05_pathOps import pathSplitChar
from .block06_stampOps import unixStampToTupleOfStrs
from .z_utils import padFlags


""" Preprocessing """

def padSegFlags(stakLog, pSegFlagsBySegFlags={}):
    # type: (Log[Tup[float, str, str, SplitLink]], Dic[str, str]) -> Dic[str, str]
    if not pSegFlagsBySegFlags:
        segFlags = list(set(entry[1] for entry in stakLog))
        paddedFlags = padFlags(segFlags)
        for segFlag, pSegFlag in izip(segFlags, paddedFlags):
            pSegFlagsBySegFlags[segFlag] = pSegFlag

    return pSegFlagsBySegFlags

def trimFilePathAddLineNum(filePath, lineno, methName, splitChar=pathSplitChar):  # type: (str, int, str, str) -> Tup[str, str]
    splitPath = filePath.split(splitChar)
    return (
        '{}{}{}{}.'.format(
            splitPath[-2],
            splitChar,
            splitPath[-1].rstrip('py'),
            lineno
        ),
        methName
    )

def trimFilePathsAddLineNums(callChain, trimmer=trimFilePathAddLineNum):
    # type: (Tup[SplitLink, ...], Cal[[SplitLink], Tup[str, str]]) -> Tup[Uni[Tup[str, str], Tup[Lst[str], str]], ...]
    for link in callChain:
        if len(link) == 2:
            yield link
        else:
            yield trimmer(*link)

def preProcessStakLog(stakLog, locsFlag=omrolocsFlag, toStr=unixStampToTupleOfStrs, trimmer=trimFilePathsAddLineNums):
    # type: (Log[Tup[float, str, str, Uni[str, SplitLink]]], str, Cal[[float], Str4], Cal) -> Itrt[Tup[float, str, str, Uni[str, Tup[SplitLink, ...]]]]
    """ Turn the unix stamps to tuples of strs, trim file path to the last two elements, add lineno to it &
    pad the segFlags."""

    pSegFlagsBySegFlags = padSegFlags(stakLog)  # Segregator flags are added dynamically, so can't be pre-padded
    for unixStamp, segFlag, callerFlag, theRest in stakLog:
        yield (
            toStr(unixStamp), pSegFlagsBySegFlags[segFlag], callerFlag,
            tuple(trimmer(theRest)) if callerFlag == locsFlag else theRest
        )


""" Links join """

def mroLinkToStrLink(mroClsNs, methName):  # type: (Lst[str], str) -> str
    mroClsNs[-1] = '{}.{}{}'.format(mroClsNs[-1], methName, ')' * (len(mroClsNs) - 1))
    return '('.join(mroClsNs)

def linksJoin(splitLinkCallChain, linker=mroLinkToStrLink):
    # type: (Tup[Uni[Tup[str, str], Tup[Lst[str], str]], ...], Cal[[Lst[str], str], str]) -> Itrt

    for bigNameSpace, methName in splitLinkCallChain:
        if isinstance(bigNameSpace, str):
            yield bigNameSpace + methName
        else:
            yield linker(bigNameSpace[:], methName)

def entriesWithLinksJoin(preProcStakLog, _omrolocsFlag=omrolocsFlag):
    # type: (Itrt[Tup[float, str, str, Uni[str, Tup[Uni[Tup[str, str], Tup[Lst[str], str]], ...]]], ...], str) -> Itrt[Tup[Str4, str, str, Uni[str, Tup[str, ...]]]]

    for stamp, segFlag, callerFlag, theRest in preProcStakLog:
        if callerFlag == _omrolocsFlag:
            yield stamp, segFlag, callerFlag, tuple(linksJoin(theRest))
        else:
            yield stamp, segFlag, callerFlag, theRest


""" Log splice """

def spliceStakLogWithStdLog(stdLogPrefix, stdLog, stakLog):
    # type: (str, Tup[Tup[Str4, str, str], ...], Tup[Tup[Str4, str, str, str], ...]) -> Itrt[Tup[Str4, str, str]]

    stdIdx, stakIdx = 0, 0
    stdElLeft, stakElLeft = True, True
    lenStd, lenStak = len(stdLog), len(stakLog)

    stdStamp, stdFlag            , stdTheRest = stdLog[stdIdx]
    stamp   , segFlag, callerFlag, theRest    = stakLog[stakIdx]

    while stdElLeft or stakElLeft:

        if stdElLeft is True and (stdStamp <= stamp or stakElLeft is False):
            yield stdStamp, stdLogPrefix, allPflagsByFlags[stdFlag], stdTheRest
            stdIdx += 1
            if stdIdx == lenStd:
                stdElLeft = False
            else:
                newStamp, stdFlag, stdTheRest = stdLog[stdIdx]
                if newStamp is not None:
                    stdStamp = newStamp

        if stakElLeft is True and (stdStamp > stamp or stdElLeft is False):
            yield stamp, segFlag, allPflagsByFlags[callerFlag], theRest
            stakIdx += 1
            if stakIdx == lenStak:
                stakElLeft = False
            else:
                stamp, segFlag, callerFlag, theRest = stakLog[stakIdx]

def stdStakSplice(stdLogs, stakLog):
    # type: (Tup[Tup[Tup[Str4, str, str], ...], ...], Tup[Tup[Str4, str, str, str], ...]) -> Lst[Lst[Tup[Str4, str, str]]]
    return [
        list(spliceStakLogWithStdLog(prefix, stdLog, stakLog))
        for prefix, stdLog in zip(stdLogPrefixes, stdLogs)
    ]
