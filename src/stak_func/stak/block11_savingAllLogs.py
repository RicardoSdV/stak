from functools import partial

from .block00_typing import *
from .block02_commonData import pStdFlagsByStdFlags, allPflagsByFlags, pOmrolocsFlag, pDataFlag, pDateFlag, omrolocsFlag, dataFlag, labelFlag, dateFlag
from .block03_log import log
from .block04_pathOps import makeDirPaths, genPrimiStakPaths, genPrimiStdPaths, genCompStakPaths, genStdStakSplicePaths, genCompStdStakSplicePaths
from .block05_stampOps import tupleOfStrsToStr, unixStampToTupleOfStrs
from .block06_creatingMroCallChains import pathSplitChar
from .block09_compression import compressLines, compressLinks
from .block10_parsingStdLogs import parseStdLogs

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
    for stamp, flag, theRest in splicedLog:
        yield toStr(stamp) + flag + theRest


def formatCompStdStakSplice(compressedStakSplice):  # type: (Lst[str]) -> Lst[str]
    return compressLines([el[-1] for el in compressedStakSplice])

def writeLogsToFile(pathGen, formatter, *logs):  # type: (Itrt[str], Cal[[Itrb], Opt[Itrb[str]]], Itrb) -> None
    for _log in logs:
        path = next(pathGen)
        with open(path, 'w') as _file:
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

def trimFilePathAddLineno(callChain, splitChar=pathSplitChar):
    # type: (Tup[Uni[Tup[str, int, str], Tup[Lst[str], str]], ...], str) -> Tup[Uni[Tup[str, str], Tup[Lst[str], str]], ...]

    # Trims path to its last two elements, adds lineno to it, yields this plus the method name
    for link in callChain:
        if len(link) == 2:  # If len is 2 its an mro link
            yield link
        else:
            filePath, lineno, methName = link
            splitPath = filePath.split(splitChar)
            yield (
                '{}{}{}{}'.format(
                    splitPath[-2],
                    splitChar,
                    splitPath[-1].rstrip('py'),
                    lineno
                ),
                methName
            )

def mroLinkToStrLink(mroClsNs, methName):  # type: (Lst[str], str) -> str
    mroClsNs[-1] = '{}.{}{}'.format(mroClsNs[-1], methName, ')' * (len(mroClsNs) - 1))
    return '('.join(mroClsNs)

def preProcessLog(_omrolocsFlag=omrolocsFlag, toStr=unixStampToTupleOfStrs):
    # type: (str, Cal[[float], Str4]) -> Itrt[Tup[float, str, Uni[str, Tup[Uni[Tup[str, str], Tup[Lst[str], str]], ...]]], ...]
    """ Turn the unix stamps to tuples of strs, trim file path to the last two elements, add lineno to it. """
    for unixStamp, flag, theRest in log:
        yield toStr(unixStamp), flag, tuple(trimFilePathAddLineno(theRest)) if flag == omrolocsFlag else theRest

def makeFullStrLinkCallChains(linker=mroLinkToStrLink, _omrolocsFlag=omrolocsFlag):
    # type: (Cal[Lst[str], str], str) -> Itrt[Tup[Str4, str, Uni[str, Tup[str, ...]]]]

    for stamp, flag, theRest in preProcessLog():
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

def saveAll():
    makeDirPaths()

    fullStrLinkCallChains = tuple(makeFullStrLinkCallChains())

    savePrimiStak(fullStrLinkCallChains)

    callChainsWithCompressedStrLinks = tuple(compressLinks(fullStrLinkCallChains))
    saveCompStak(callChainsWithCompressedStrLinks)

    # Flags not padded yet
    parsedStdLogs = tuple(parseStdLogs())  # type: Tup[Tup[Tup[Str4, str, str], ...], ...]

    savePrimiStd(*parsedStdLogs)

    splicedLogs = stdStakSplice(parsedStdLogs, callChainsWithCompressedStrLinks)

    saveStdStakSplice(*splicedLogs)

    saveCompStdStakSplice(*splicedLogs)




## Out of service: The idea was that sometimes the entire MRO would be unnecessary,
# but it seems that most classes don't have an inheritance chain big enough to be a problem
# def partStrLinkCreator(mroClsNs, methName):  # type: (Lst[str], str) -> str
#     return mroClsNs[-1] + methName
