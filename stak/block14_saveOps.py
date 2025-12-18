from .block00_autoImports import *


def joinSplitLinksAndLeaveOutSilencedFiles():  # type: () -> Lst[Str4, Tup[str, ...]]
    strLinkStakLog = []; append = strLinkStakLog.append
    silencedFound = set(); addSilencedFound = silencedFound.add
    for stamp, theRest in stakLog:

        firstFrameFilePath = theRest[0][0]

        if firstFrameFilePath:
            if firstFrameFilePath in silentFiles:
                continue

            if loudFiles:
                if not any(path in firstFrameFilePath for path in loudFiles):
                    addSilencedFound(firstFrameFilePath)
                    continue

            if silentFiles:
                if any(path in firstFrameFilePath for path in silentFiles):
                    addSilencedFound(firstFrameFilePath)
                    continue

        if theRest.__class__ is not str:
            theRest = tuple(joinLinks(theRest))  # Is splitLinks

        append((floatToStr4(stamp), theRest))

    return strLinkStakLog

def savePrimitiveStak(strLinkStakLog):
    if saveStakPrimi:
        path = getPrimiStakPath()

        formattedPrimiStak = [
            str4ToStr(stamp) + ': ' + strLinks + '\n'  # Is date or event label
            if strLinks.__class__ is str
            else
            str4ToStr(stamp) + ': ' + ' <- '.join(strLinks) + '\n'

            for stamp, strLinks in strLinkStakLog
        ]

        writeLines(path, formattedPrimiStak)

def compressAndSaveStak(compCallChainsStak):
    if saveStakComp:
        path = getCompStakPath()
        prettyCompressedLines = prettyCompressLines(compCallChainsStak)
        writeLines(path, prettyCompressedLines)

def saveStakLog():
    strLinkStakLog = joinSplitLinksAndLeaveOutSilencedFiles()

    if len(strLinkStakLog) <= 1:
        print '[STAK] ERROR: Trying to save stak log but all silenced: silent=%s, loud=%s' % (silentFiles, loudFiles)
        return

    savePrimitiveStak(strLinkStakLog)
    compCallChainsStak = compressCallChains(strLinkStakLog)
    compressAndSaveStak(compCallChainsStak)

def saveAll():
    start = clock()
    makeDirPaths()

    if len(stakLog) > 1:
        saveStakLog()

    if traceLog:
        saveTraceLog(traceLog)

    print '[STAK] saveAll finished, lines=%s, took=%s, silentFiles=%s, loudFiles=%s' % (len(stakLog), clock() - start, silentFiles, loudFiles)


# TODO: There is now no settings object, must rethink pickling, what about saving an entire copy of stak?
def picklePrimitiveLogs():
    return
    # if so.saveStakPickle or saveTracePickle:
    #     logDict = {'settings': so.toDict()}
    #     if so.saveStakPickle : logDict['stakLog']  = stakLog
    #     if so.saveTracePickle: logDict['traceLog'] = traceLog
    #     writePickle(po.getPicklePath(), logDict)

def loadAndResave(path=''):
    return
    # path = path or loadAndResavePath
    # oldSettingsDict = so.toDict()
    #
    # logs = readPickle(path)
    #
    # if so.overrideSettingsOnLAR:
    #     newSettingsDict = logs['settings']
    #     so.fromDict(newSettingsDict)
    #
    # # The base logs are not changed on resave,
    # # no reason to save a copy.
    # so.saveStakPickle  = 0
    # so.saveTracePickle = 0
    #
    # oldStakLog = stakLog[:]
    # oldTraceLog = copy(traceLog)
    #
    # stakLog[:] = logs['stakLog']
    # traceLog.clear()
    # traceLog.extend(logs['traceLog'])
    #
    # saveAll()
    #
    # so.fromDict(oldSettingsDict)
    # stakLog[:] = oldStakLog
    # traceLog.clear()
    # traceLog.extend(oldTraceLog)
