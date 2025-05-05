import json
from functools import partial
from itertools import izip

from .block00_typing import *
from .block02_settingObj import so
from . import block03_constants as cs
from .block04_log import log
from .block05_pathOps import getPrimiStakPaths, getPrimiStdPaths, getCompStakPaths, getStdStakSplicePaths, getCompStdStakSplicePaths, getTracePaths, getCompactTracePaths, makeDirPaths, getJsonPath
from .block06_stampOps import tupleOfStrsToStr, unixStampToStr, unixStampToTupleOfStrs
from .block09_joinSplitLinks import joinLink, joinLinks
from .block12_compression import compressLines, compressCallChains
from .block13_parseStdLogs import parseStdLogs
from .block14_fmtStakAndStd import stdStakSplice
from .z_utils import write, redStr

# In general the working theory is that we don't care too much about performance when saving logs, if in exchange
# performance is gained when generating, because generation takes place during critical parts of the program
# whereas saving is normally done during idle periods. This explains some of the wierd decisions.
# Saving is quite slow though, but the main bottleneck is in compression not here.

def formatPrimiStak(strLinksStakLog, toStr=tupleOfStrsToStr):  # type: (Itrb[Tup[Str4, Uni[str, Tup[str, ...]]]], ...) -> Itrt[str]
    for stamp, strLinks in strLinksStakLog:
        if type(strLinks) is tuple:
            strLinks = ' <- '.join(strLinks)
        yield toStr(stamp) + ': ' + strLinks

def formatPrimiStd(parsedStdLog, toStr=tupleOfStrsToStr, pFlags=cs.pStdFlagsByStdFlags):
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

def fmtSetEntry(stamp, splitLink, toStr=unixStampToStr, flag=cs.pSetFlag, join=joinLink):
    # type: (float, Uni[Tup[str, int, str], Tup[Lst[str], str]], Cal[[float], str], str, Cal[[Uni[Tup[str, int, str], Tup[Lst[str], str]]], str]) -> str
    return toStr(stamp) + flag + join(splitLink)

def fmtCallEntry(stamp, splitLink, toStr=unixStampToStr, flag=cs.pCallFlag, join=joinLink):
    # type: (float, Uni[Tup[str, int, str], Tup[Lst[str], str]], Cal[[float], str], str, Cal[[Uni[Tup[str, int, str], Tup[Lst[str], str]]], str]) -> str
    return toStr(stamp) + flag + join(splitLink)

def fmtRetEntry(stamp, splitLink, toStr=unixStampToStr, flag=cs.pRetFlag, join=joinLink):
    # type: (float, Uni[Tup[str, int, str], Tup[Lst[str], str]], Cal[[float], str], str, Cal[[Uni[Tup[str, int, str], Tup[Lst[str], str]]], str]) -> str
    return toStr(stamp) + flag + join(splitLink)

def fmtDelEntry(stamp, splitLink, toStr=unixStampToStr, flag=cs.pDelFlag, join=joinLink):
    # type: (float, Uni[Tup[str, int, str], Tup[Lst[str], str]], Cal[[float], str], str, Cal[[Uni[Tup[str, int, str], Tup[Lst[str], str]]], str]) -> str
    return toStr(stamp) + flag + join(splitLink)

def formatTrace(traceEntries, formattersByFlag={cs.setFlag: fmtSetEntry, cs.callFlag: fmtCallEntry, cs.retFlag: fmtRetEntry, cs.delFlag: fmtDelEntry}):
    for stamp, flag, theRest in traceEntries:
        yield formattersByFlag[flag](stamp, theRest)

def formatCompactTrace(entries): return entries

def writeLogsToFile(pathsGetter, formatter, *logs):  # type: (Cal[[], Itrb[str]], Cal[[Itrb], Opt[Itrb[str]]], Itrb) -> None
    paths = pathsGetter()
    for _log, path in izip(logs, paths):
        formattedLines = formatter(_log)
        if formattedLines:
            # Yes, it's been tried, ONLY ADD NEW LINES AT THE END! it's been tried more than once
            # for some reason it never ends well, just loop over the log once more, not a big
            # deal, it's been tried, don't do IT! (I'll probably try a third time...)
            lines = (line + '\n' for line in formattedLines)
            write(path, lines)

savePrimiStak         = partial(writeLogsToFile, getPrimiStakPaths        , formatPrimiStak)
savePrimiStd          = partial(writeLogsToFile, getPrimiStdPaths         , formatPrimiStd)
saveCompStak          = partial(writeLogsToFile, getCompStakPaths         , formatCompStak)
saveStdStakSplice     = partial(writeLogsToFile, getStdStakSplicePaths    , formatStdStakSplice)
saveCompStdStakSplice = partial(writeLogsToFile, getCompStdStakSplicePaths, formatCompStdStakSplice)
saveTrace             = partial(writeLogsToFile, getTracePaths            , formatTrace)
saveCompactTrace      = partial(writeLogsToFile, getCompactTracePaths     , formatCompactTrace)

def saveRawLogAsJson():
    logDict = {
        'settings': so.toDict(),
        'stakLog': log,
    }
    with open(getJsonPath(), 'w') as f:
        json.dump(logDict, f)

def entriesWithLinksJoin(stakLog, joinLinks=joinLinks, toTuple=unixStampToTupleOfStrs):  # type: (Lst[Tup[float, Uni[Tup[SplitLink, ...], str]]], ..., ...) -> Itrt[Tup[Str4, Uni[Tup[str, ...], str]]]
    silenced = so.silencedFiles

    for stamp, theRest in stakLog:
        firstFrameFilePath = theRest[0][0]
        if firstFrameFilePath in silenced and silenced[firstFrameFilePath]:
            continue

        if isinstance(theRest, tuple):  # Is splitLinks
            theRest = tuple(joinLinks(theRest))

        yield toTuple(stamp), theRest

def saveStakLog():
    saveRawLogAsJson()

    strLinkStakLog = tuple(entriesWithLinksJoin(log))

    if len(strLinkStakLog) <= 1:
        print redStr('ERROR: Trying to save stak log but all silenced')
        return

    compCallChainsStakLog = tuple(compressCallChains(strLinkStakLog))
    parsedStdLogs = tuple(parseStdLogs())
    stakAndStdSplices = stdStakSplice(parsedStdLogs, compCallChainsStakLog)

    savePrimiStak(strLinkStakLog)
    saveCompStak(compCallChainsStakLog)
    savePrimiStd(*parsedStdLogs)
    saveStdStakSplice(*stakAndStdSplices)
    saveCompStdStakSplice(*stakAndStdSplices)

def saveAll():
    makeDirPaths()

    if len(log) > 1:
        saveStakLog()

# def saveAll():
#     makeDirPaths()
#
#     if len(log) > 1:
#         strLinkStakLog = tuple(entriesWithLinksJoin(log))
#         compCallChainsStakLog = tuple(compressCallChains(strLinkStakLog))
#         parsedStdLogs = tuple(parseStdLogs())
#         stakAndStdSplices = stdStakSplice(parsedStdLogs, compCallChainsStakLog)
#
#         savePrimiStak(strLinkStakLog)
#         saveCompStak(compCallChainsStakLog)
#         savePrimiStd(*parsedStdLogs)
#         saveStdStakSplice(*stakAndStdSplices)
#         saveCompStdStakSplice(*stakAndStdSplices)
#
#     if traceLog:
#         formattedTraceLog = formatTraceLog(traceLog)
#         saveCompactTrace(formattedTraceLog)

















## Out of service: The idea was that sometimes the entire MRO would be unnecessary,
# but it seems that most classes don't have an inheritance chain big enough to be a problem
# def partStrLinkCreator(mroClsNs, methName):  # type: (Lst[str], str) -> str
#     return mroClsNs[-1] + methName
