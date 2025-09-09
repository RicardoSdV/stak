from copy import copy

from         .block00_typing         import *
from         .block02_settingObj     import so
from . import block03_constants          as cs
from         .block04_log            import stakLog, traceLog
from . import block05_pathOps            as po
from         .block06_stampOps       import str4ToStr, floatToStr4
from         .block08_joinLinks      import joinLinks
from         .block10_tracing        import saveTraceLog
from         .block11_compression    import compressCallChains, prettyCompressLines
from         .block12_parseStdLogs   import parseLines, interpolLines
from         .block15_utils          import write, writePickle, read, readPickle, log


def joinSplitLinksAndLeaveOutSilencedFiles(
        _joinLinks=joinLinks,  # type: Cal[[Itrb[SplitLink]], Itrt[str]]
        _floatToStr4=floatToStr4,  # type: Cal[[float], Str4]
):  # type: (...) -> Lst[Str4, Tup[str, ...]]

    silentPaths = so.silentFiles
    loudPaths = so.loudFiles

    strLinkStakLog = []; append = strLinkStakLog.append
    silencedFound = set(); addSilencedFound = silencedFound.add
    for stamp, theRest in stakLog:

        firstFrameFilePath = theRest[0][0]

        if firstFrameFilePath:
            if firstFrameFilePath in silentPaths:
                continue

            if loudPaths:
                if not any(path in firstFrameFilePath for path in loudPaths):
                    addSilencedFound(firstFrameFilePath)
                    continue

            if silentPaths:
                if any(path in firstFrameFilePath for path in silentPaths):
                    addSilencedFound(firstFrameFilePath)
                    continue

        if theRest.__class__ is not str:
            theRest = tuple(_joinLinks(theRest))  # Is splitLinks

        append((_floatToStr4(stamp), theRest))

    return strLinkStakLog

def savePrimitiveStak(
        strLinkStakLog,
        _str4ToStr = str4ToStr,  # type: Cal[[Str4], str]
):
    if so.saveStakPrimi:
        path = po.getPrimiStakPath()

        formattedPrimiStak = [
            _str4ToStr(stamp) + ': ' + strLinks + '\n'  # Is date or event label
            if strLinks.__class__ is str
            else
            _str4ToStr(stamp) + ': ' + ' <- '.join(strLinks) + '\n'

            for stamp, strLinks in strLinkStakLog
        ]

        write(path, formattedPrimiStak)

def compressAndSaveStak(compCallChainsStak):
    if so.saveStakComp:
        path = po.getCompStakPath()
        prettyCompressedLines = prettyCompressLines(compCallChainsStak)
        write(path, prettyCompressedLines)

def readAndParseStdLog(prefix):
    readPath = po.getStdLogPath(prefix)
    rawStdLog = read(readPath)
    parsedLines = parseLines(rawStdLog)
    interpoledLines = interpolLines(parsedLines)
    parsedStdLog = [
        ((hour, minute, second, millisec), flag, theRest.rstrip('\n'))
        for year, month, day, hour, minute, second, millisec, flag, theRest in interpoledLines
    ]
    return parsedStdLog

def saveStdLogToPrimitives(
        prefix,
        parsedStdLog,
        _str4ToStr = str4ToStr,
        _pFlags    = cs.pStdFlagsByStdFlags,
):
    if so.saveStdPrimi:
        path = po.getPrimiStdPath(prefix)
        log = (
            _str4ToStr(stamp) + _pFlags[stdFlag] + theRest + '\n'
            for stamp, stdFlag, theRest in parsedStdLog
        )
        write(path, log)

def spliceStakAndStdLog(
        parsedStdLog,
        compCallChainsStak,
        _allPflags = cs.allPflagsByFlags,  # type: Dic[str, str]
        stdIdx=0, stakIdx=0, stdElLeft=True, stakElLeft=True,
):
    stdStakSpliced = []; append = stdStakSpliced.append
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

    return stdStakSpliced

def saveUncompressedSplice(
        prefix,
        stdStakSpliced,
        _str4ToStr = str4ToStr,  # type: Cal[[Str4], str]
):
    if so.saveStdStakSplice:
        log = (
            (_str4ToStr(stamp) + flag + theRest + '\n')
            for stamp, flag, theRest in stdStakSpliced
        )
        path = po.getStdStakSplicePath(prefix)
        write(path, log)

def compressAndSaveCompressedSplice(prefix, stdStakSpliced):
    if so.saveStdStakSpliceComp:
        path = po.getCompStdStakSplicePath(prefix)
        prettyCompressedSplice = prettyCompressLines(stdStakSpliced)
        write(path, prettyCompressedSplice)

def saveStakLog():
    strLinkStakLog = joinSplitLinksAndLeaveOutSilencedFiles()

    if len(strLinkStakLog) <= 1:
        log('Trying to save stak log but all silenced: silent=%s, loud=%s' % (so.silentFiles, so.loudFiles))
        return

    savePrimitiveStak(strLinkStakLog)
    compCallChainsStak = compressCallChains(strLinkStakLog)
    compressAndSaveStak(compCallChainsStak)

    if not (so.saveStdStakSplice and so.saveStdStakSpliceComp and so.saveStdPrimi):
        return

    for prefix in so.stdLogPrefixes:
        parsedStdLog = readAndParseStdLog(prefix)
        saveStdLogToPrimitives(prefix, parsedStdLog)

        if not (so.saveStdStakSplice and so.saveStdStakSpliceComp):
            continue

        stdStakSpliced = spliceStakAndStdLog(parsedStdLog, compCallChainsStak)
        saveUncompressedSplice(prefix, stdStakSpliced)
        compressAndSaveCompressedSplice(prefix, stdStakSpliced)

def picklePrimitiveLogs():
    if so.saveStakPickle or so.saveTracePickle:
        logDict = {'settings': so.toDict()}
        if so.saveStakPickle : logDict['stakLog']  = stakLog
        if so.saveTracePickle: logDict['traceLog'] = traceLog
        writePickle(po.getPicklePath(), logDict)

def saveAll():
    po.makeDirPaths()

    if len(stakLog) > 1:
        saveStakLog()

    if traceLog:
        saveTraceLog(traceLog)

def loadAndResave(path=''):
    path = path or so.loadAndResavePath
    oldSettingsDict = so.toDict()

    logs = readPickle(path)

    if so.overrideSettingsOnLAR:
        newSettingsDict = logs['settings']
        so.fromDict(newSettingsDict)

    # The base logs are not changed on resave,
    # no reason to save a copy.
    so.saveStakPickle  = 0
    so.saveTracePickle = 0

    oldStakLog = stakLog[:]
    oldTraceLog = copy(traceLog)

    stakLog[:] = logs['stakLog']
    traceLog.clear()
    traceLog.extend(logs['traceLog'])

    saveAll()

    so.fromDict(oldSettingsDict)
    stakLog[:] = oldStakLog
    traceLog.clear()
    traceLog.extend(oldTraceLog)
