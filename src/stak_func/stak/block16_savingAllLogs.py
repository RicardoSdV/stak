from functools import partial

from .block00_typing import *
from .block03_commonData import pOmrolocsFlag, pDataFlag, pDateFlag, omrolocsFlag, daffFlag, labelFlag, dateFlag, pStdFlagsByStdFlags, pSetFlag, pCallFlag, pRetFlag, pDelFlag, setFlag, callFlag, retFlag, delFlag, allPflagsByFlags, traceFlags, callableNames, callFlags, retFlags
from .block05_log import traceLog, log
from .block06_pathOps import makeDirPaths, genPrimiStakPaths, genPrimiStdPaths, genCompStakPaths, genStdStakSplicePaths, genCompStdStakSplicePaths, genTracePaths, genCompactTracePaths
from .block07_stampOps import tupleOfStrsToStr, unixStampToStr
from .block09_creatingMroCallChains import joinFileLink, joinMroLink
from .block12_compression import compressLines, compressCallChains
from .block13_parseStdLogs import parseStdLogs
from .block14_fmtStakAndStd import preProcessStakLog, entriesWithLinksJoin, stdStakSplice
from .block15_fmtTrace import formatTraceLog

# In general the working theory is that we don't care too much about performance when saving logs, if in exchange
# performance is gained when generating, because generation takes place during critical parts of the program
# whereas saving is normally done during idle periods. This explains some of the wierd decisions.
# Saving is quite slow though, but the main bottleneck is in compression not here.

def fmtOmrolocsEntry(stamp, segFlag, theRest, toStr=tupleOfStrsToStr, callerFlag=pOmrolocsFlag):  # type: (Str4, str, str, Cal[[Str4], str], str) -> str
    return toStr(stamp) + segFlag + callerFlag + ' <- '.join(theRest)

def fmtDataEntry(stamp, segFlag, theRest, toStr=tupleOfStrsToStr, flag=pDataFlag):  # type: (Str4, str, str, Cal[[Str4], str], str) -> str
    return toStr(stamp) + segFlag + flag + theRest

def fmtLabelEntry(_, theRest):  # type: (Str4, str) -> str
    return theRest

def fmtDateEntry(stamp, segFlag, theRest, toStr=tupleOfStrsToStr, flag=pDateFlag):  # type: (Str4, str, str, Cal[[Str4], str], str) -> str
    return toStr(stamp) + segFlag + flag + theRest

def formatPrimiStak(fullStrLinkCallChains, formattersByFlag={omrolocsFlag: fmtOmrolocsEntry, daffFlag: fmtDataEntry, labelFlag: fmtLabelEntry, dateFlag: fmtDateEntry}):
    # type: (Tup[Tup[Str4, str, Uni[str, Lst[str]]], ...], Dic[str, Cal[[Str4, str, str], str]]) -> Itrt[str]
    for stamp, segFlag, callerFlag, theRest in fullStrLinkCallChains:
        yield formattersByFlag[callerFlag](stamp, segFlag, theRest)

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
    for stamp, segFlag, callerFlag, theRest in splicedLog:
        yield toStr(stamp) + segFlag + callerFlag + theRest

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


def saveAll():
    makeDirPaths()

    if len(log) > 1:
        preProcessedStakLog = preProcessStakLog(log)
        strLinkStakLog = tuple(entriesWithLinksJoin(preProcessedStakLog))
        compCallChainsStakLog = tuple(compressCallChains(strLinkStakLog))
        parsedStdLogs = tuple(parseStdLogs())
        stakAndStdSplices = stdStakSplice(parsedStdLogs, compCallChainsStakLog)

        savePrimiStak(strLinkStakLog)
        saveCompStak(compCallChainsStakLog)
        savePrimiStd(*parsedStdLogs)
        saveStdStakSplice(*stakAndStdSplices)
        saveCompStdStakSplice(*stakAndStdSplices)

    if traceLog:
        formattedTraceLog = formatTraceLog()
        saveCompactTrace(formattedTraceLog)

















## Out of service: The idea was that sometimes the entire MRO would be unnecessary,
# but it seems that most classes don't have an inheritance chain big enough to be a problem
# def partStrLinkCreator(mroClsNs, methName):  # type: (Lst[str], str) -> str
#     return mroClsNs[-1] + methName
