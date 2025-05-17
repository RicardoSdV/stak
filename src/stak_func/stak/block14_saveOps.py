from itertools import izip

from         .block00_typing import *
from         .block02_settingObj import so
from . import block03_constants as cs
from         .block04_log import stakLog, traceLog
from . import block05_pathOps as po
from         .block06_stampOps import tupleOfStrsToStr, unixStampToStr, unixStampToTupleOfStrs
from         .block08_joinSplitLinks import joinLink, joinLinks
from         .block11_compression import compressCallChains, prettyCompressLines
from         .block12_parseStdLogs import parseStdLog
from         .block13_fmtTrace import compactTraceLog
from         .z_utils import write, writeJson, writeGzip, E, read


def saveRawLogsToJson(stakLog, traceLog):
    if so.saveJsonStak or so.saveJsonTrace:
        logDict = {'settings': so.toDict()}
        if so.saveJsonStak : logDict['stakLog'] = stakLog
        if so.saveJsonTrace: logDict['traceLog'] = traceLog
        writeJson(po.getJsonPath(), logDict)

    if so.saveZipStak or so.saveZipTrace:
        logDict = {'settings': so.toDict()}
        if so.saveZipStak : logDict['stakLog'] = stakLog
        if so.saveZipTrace: logDict['traceLog'] = traceLog
        writeGzip(po.getZippedPath(), logDict)

def entriesWithLinksJoin(stakLog, joinLinks=joinLinks, toTuple=unixStampToTupleOfStrs):  # type: (Lst[Tup[float, Uni[Tup[SplitLink, ...], str]]], ..., ...) -> Itrt[Tup[Str4, Uni[Tup[str, ...], str]]]
    silenced = so.silencedFiles

    for stamp, theRest in stakLog:
        firstFrameFilePath = theRest[0][0]
        if firstFrameFilePath in silenced and silenced[firstFrameFilePath]:
            continue

        if isinstance(theRest, tuple):  # Is splitLinks
            theRest = tuple(joinLinks(theRest))

        yield toTuple(stamp), theRest

def saveTraceLog(
        toStr    = unixStampToStr,
        joinLink = joinLink,  # type: Cal[[SplitLink], str]
        padByNot = {noPad: pad for noPad, pad in izip(cs.traceFlags, cs.pTraceFlags)}
):

    if so.saveTrace:
        fmtdTrace = (
            toStr(stamp) + padByNot[flag] + joinLink(splitLink) + '\n'
            for stamp, flag, splitLink in traceLog
        )
        path = po.getTracePath()
        write(path, fmtdTrace)

    if so.saveCompactTrace:
        compactedTraceLog = compactTraceLog(traceLog)
        path = po.getCompactTracePath()
        write(path, compactedTraceLog)

def saveStakLog(
        _toStr     = tupleOfStrsToStr,
        _pFlags    = cs.pStdFlagsByStdFlags,
        _allPflags = cs.allPflagsByFlags,
        _joinLinks = joinLinks,
):
    strLinkStakLog = tuple(entriesWithLinksJoin(stakLog))

    if len(strLinkStakLog) <= 1:
        E('Trying to save stak log but all silenced')
        return

    compCallChainsStak = tuple(compressCallChains(strLinkStakLog))

    if so.savePrimiStak:
        path = po.getPrimiStakPath()

        formattedPrimiStak = [
                _toStr(stamp) + ': ' + ' <- '.join(strLinks) + '\n'
            if strLinks.__class__ is tuple
            else
                _toStr(stamp) + ': ' + strLinks + '\n'  # Is date or event label

            for stamp, strLinks in strLinkStakLog
        ]

        write(path, formattedPrimiStak)

    if so.saveCompStak:
        path = po.getCompStakPath()
        prettyCompressedLines = prettyCompressLines(compCallChainsStak)
        write(path, prettyCompressedLines)

    saveStdStakSplice = so.saveStdStakSplice
    saveCompStdStakSplice = so.saveCompStdStakSplice
    saveSplices = saveStdStakSplice or saveCompStdStakSplice

    if not saveSplices and not so.savePrimiStd:
        return

    for prefix in so.stdLogPrefixes:
        readPath = po.getStdLogPath(prefix)
        rawStdLog = read(readPath)

        parsedStdLog = tuple(parseStdLog(rawStdLog))

        if so.savePrimiStd:
            path = po.getPrimiStdPath(prefix)
            log = (
                _toStr(stamp) + _pFlags[stdFlag] + theRest + '\n'
                for stamp, stdFlag, theRest in parsedStdLog
            )
            write(path, log)

        if not saveSplices:
            continue

# Splice stak and std logs.
# -------------------------------------------------------------------------------------------------
        stdStakSpliced = []; append = stdStakSpliced.append

        stdIdx = 0; stakIdx = 0
        stdElLeft = True; stakElLeft = True
        lenStd = len(parsedStdLog); lenStak = len(stakLog)

        stdStamp, stdFlag, stdTheRest = parsedStdLog[stdIdx]
        stamp, theRest = compCallChainsStak[stakIdx]

        while stdElLeft or stakElLeft:

            if stdElLeft is True and (stdStamp <= stamp or stakElLeft is False):
                append((stdStamp, _allPflags[stdFlag], stdTheRest))
                stdIdx += 1
                if stdIdx == lenStd:
                    stdElLeft = False
                else:
                    newStamp, stdFlag, stdTheRest = parsedStdLog[stdIdx]
                    if newStamp is not None:
                        stdStamp = newStamp

            if stakElLeft is True and (stdStamp > stamp or stdElLeft is False):
                append((stamp, '', theRest))  # todo: stak flags
                stakIdx += 1
                if stakIdx == lenStak:
                    stakElLeft = False
                else:
                    stamp, theRest = compCallChainsStak[stakIdx]
# -------------------------------------------------------------------------------------------------

        if saveStdStakSplice:
            log = (
                (_toStr(stamp) + flag + theRest + '\n')
                for stamp, flag, theRest in stdStakSpliced
            )
            path = po.getStdStakSplicePath(prefix)
            write(path, log)

        if saveCompStdStakSplice:
            path = po.getCompStdStakSplicePath(prefix)
            prettyCompressedSplice = prettyCompressLines(stdStakSpliced)
            write(path, prettyCompressedSplice)


def saveAll():
    po.makeDirPaths()

    saveRawLogsToJson(stakLog, traceLog)

    if len(stakLog) > 1:
        saveStakLog()

    if traceLog:
        saveTraceLog()
