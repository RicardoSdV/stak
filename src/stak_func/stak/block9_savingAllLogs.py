from functools import partial
from os.path import join, splitext, basename, dirname, isfile

from .block0_typing import *
from .block1_commonData import stakFlags, pStakFlags, pStdFlagsByStdFlags, allPflagsByFlags, stdLogFiles, traceLog, log
from .block2_pathOps import pathLogStak, pathLogTrace, pathLogsStd, pathDirVari, addSuffix, pathDirPrint, makeDirPaths
from .block3_stampOps import tupleOfStrsToStr, unixStampToTupleOfStrs
from .block4_creatingMroCallChains import pathSplitChar
from .block6_tracing import formatTraceLog
from .block7_compression import compressLines, compressLinksGen
from .block8_parsingStdLogs import parseStdLogs


def addNewLines(log):  # type: (Itrb[str]) -> Itrt[str]
    return ('{}\n'.format(entry) for entry in log)

def formatStakLog(logWhereIfCallChainStrLinks):  # type: (Tup[Tup[Str4, str, Uni[str, Lst[str]]], ...]) -> Itrt[str]
    omrolocsFlag , dateFlag , dataFlag , labelFlag  = stakFlags
    pOmrolocsFlag, pDateFlag, pDataFlag, pLabelFlag = pStakFlags
    _tupleOfStrsToStr = tupleOfStrsToStr

    for stamp, flag, theRest in logWhereIfCallChainStrLinks:
        if flag == omrolocsFlag:
            yield '{}{}{}'.format(_tupleOfStrsToStr(stamp), pOmrolocsFlag, ' <- '.join(theRest))
        elif flag == dataFlag:
            yield '{}{}{}'.format(_tupleOfStrsToStr(stamp), pDataFlag, theRest)
        elif flag == labelFlag:
            yield theRest
        elif flag == dateFlag:
            yield '{}{}{}'.format(_tupleOfStrsToStr(stamp), pDateFlag, theRest)
        else:
            raise ValueError('Unsupported flag: {}'.format(flag))

def formatParsedStdLog(parsedStdLog):  # type: (Seq[Tup[Str4, str, str]]) -> Itrt[str]
    _tupleOfStrsToStr, _pStdFlagsByStdFlags = tupleOfStrsToStr, pStdFlagsByStdFlags
    for midStamp, stdFlag, theRest in parsedStdLog:
        yield '{}{}{}'.format(
            _tupleOfStrsToStr(midStamp),
            _pStdFlagsByStdFlags[stdFlag],
            theRest,
        )

def makeFilePathUnique(path):  # type: (str) -> str
    # Increment an integer suffix until path of file (not dir) is unique
    fileName, ext = splitext(
        basename(path)
    )
    dirPath = dirname(path)
    cnt = 0

    while isfile(path):
        cnt += 1
        path = join(
            dirPath, '{}{}{}'.format(fileName, cnt, ext)
        )

    return path

def writeLogsToFile(pathYielder, formatter, *logs):  # type: (PathGen, Cal[[Itrb], Opt[Itrb[str]]], Itrb) -> None
    for path, log in zip(pathYielder(), logs):
        with open(makeFilePathUnique(path), 'w') as logFile:
            logLines = formatter(log)
            if logLines:
                logFile.writelines(addNewLines(logLines))

saveStakLogToPrimitives  = partial(writeLogsToFile, pathLogStak, formatStakLog)
saveTraceLogToPrimitives = partial(writeLogsToFile, pathLogTrace, formatTraceLog)
saveStdLogsToPrimitives  = partial(writeLogsToFile, pathLogsStd, formatParsedStdLog)

def trimFilePathAddLineno(callChain):
    # type: (Tup[Uni[Tup[str, int, str], Tup[Lst[str], str]], ...]) -> Tup[Uni[Tup[str, str], Tup[Lst[str], str]], ...]

    # Trims path to its last to elements, adds lineno to it, yields this plus the method name
    for link in callChain:
        if len(link) == 2:
            yield link
        else:
            filePath, lineno, methName = link
            splitPath = filePath.split(pathSplitChar)
            yield (
                '{}{}{}{}'.format(
                    splitPath[-2],
                    pathSplitChar,
                    splitPath[-1].rstrip('py'),
                    lineno
                ),
                methName
            )

def preProcessLog():
    # Turn the unix stamps to tuples of strs, trim file path to the last two elements, add lineno to it.
    omrolocsFlag = stakFlags[0]
    for unixStamp, flag, theRest in log:
        if flag == omrolocsFlag:
            yield unixStampToTupleOfStrs(unixStamp), flag, tuple(trimFilePathAddLineno(theRest))
        else:
            yield unixStampToTupleOfStrs(unixStamp), flag, theRest

def strLinkCallChain(
        preprocLog,  # type: Tup[Tup[float, str, Uni[str, Tup[Uni[Tup[str, str], Tup[Lst[str], str]], ...]]], ...]
        linker       # type: Cal[Lst[str], str]
):                   # type: (...) -> Itrt[Tup[Str4, str, Uni[str, Tup[str, ...]]]]

    omrolocsFlag = stakFlags[0]
    for stamp, flag, theRest in preprocLog:
        if flag == omrolocsFlag:
            yield stamp, flag, tuple(  # At this point theRest is the splitLinkCallChain
                (
                    '{}.{}'.format(bigNameSpace, methName) if isinstance(bigNameSpace, str)
                    else linker(bigNameSpace[:], methName)
                    for bigNameSpace, methName in theRest
                )
            )
        else:
            yield stamp, flag, theRest

def mroLinkToStrLink(mroClsNs, methName):  # type: (Lst[str], str) -> str
    mroClsNs[-1] = '{}.{}{}'.format(mroClsNs[-1], methName, ')' * (len(mroClsNs) - 1))
    return '('.join(mroClsNs)

def partStrLinkCreator(mroClsNs, methName):  # type: (Lst[str], str) -> str
    return '{}.{}'.format(mroClsNs[-1], methName)

def spliceStakLogWithStdLog(stdLog, log):
    # type: (Tup[Tup[Str4, str, str], ...], Tup[Tup[Str4, str, str], ...]) -> Itrt[Tup[Str4, str, str]]

    stdIdx, stakIdx = 0, 0
    stdElLeft, stakElLeft = True, True
    lenStd, lenStak = len(stdLog), len(log)

    stdStamp, stdFlag, stdTheRest = stdLog[stdIdx]
    stamp   , flag   , theRest    = log[stakIdx]

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
                stamp, flag, theRest = log[stakIdx]

def saveSplicedToVariants(
    stdLogs,  # type: Tup[Tup[Tup[Str4, str, str], ...], ...]
    stakLog,  # type: Tup[Tup[Str4, str, str], ...]
):            # type: (...) -> Lst[Lst[Tup[Str4, str, str]]]
    splicedLogs = []
    for stdLog, logName in zip(stdLogs, stdLogFiles):

        path = makeFilePathUnique(
            join(
                next(pathDirVari()), addSuffix(logName, 'Splice')
            )
        )
        splicedLog = list(spliceStakLogWithStdLog(stdLog, stakLog))  # Need this to be list bc compression
        splicedLogs.append(splicedLog)

        with open(path, 'w') as f:
            f.writelines(
                (
                    '{}:{}:{}.{}'.format(*stamp) + flag + theRest
                    for stamp, flag, theRest in splicedLog
                )
            )

    return splicedLogs

def saveCompressedStakLogToVariants(
    logWhereIfCallChainItsStrLinksAreCompressed  # type: Tup[Tup[Str4, str, str], ...]
):
    with open(
            makeFilePathUnique(
                join(
                    next(pathDirVari()), 'stakCompress.log')
            ),
            'w'
    ) as f:
        f.writelines(
            compressLines(
                [entry[-1] for entry in logWhereIfCallChainItsStrLinksAreCompressed]
            )
        )

def saveCompressedSplicedLogs(splicedLogs):  # type: (Lst[Lst[Tup[Str4, str, str]]]) -> None
    for log, name in zip(splicedLogs, stdLogFiles):
        with open(
                makeFilePathUnique(
                    join(
                        next(pathDirPrint()), name
                    )
                ), 'w'
        ) as f:
            f.writelines(
                compressLines(
                    [el[-1] for el in log]
                )
            )

def saveAll():  # type: () -> None
    # One func to save them all...
    makeDirPaths()

    if TYPE_CHECKING:
        cast(Lst[Tup[float, str, Uni[Tup[Uni[Tup[str, int, str], Tup[Lst[str], str]], ...]]]], log)

    fullStrLinkCallChains = tuple(strLinkCallChain(preProcessLog(), mroLinkToStrLink))
    for line in fullStrLinkCallChains:
        print repr(line)

    saveStakLogToPrimitives(fullStrLinkCallChains)

    saveTraceLogToPrimitives(traceLog)

    callChainsWithCompressedStrLinks = tuple(compressLinksGen(fullStrLinkCallChains))
    saveCompressedStakLogToVariants(callChainsWithCompressedStrLinks)

    parsedStdLogs = tuple(  # Flags not padded yet
        parseStdLogs()
    )

    saveStdLogsToPrimitives(*parsedStdLogs)
    splicedLogs = saveSplicedToVariants(parsedStdLogs, callChainsWithCompressedStrLinks)

    saveCompressedSplicedLogs(splicedLogs)

