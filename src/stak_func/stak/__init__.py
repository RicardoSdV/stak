"""
This is the interface of stak, all funcs intended to be called from outside this module should be imported from here.

For convenience the entire interface can be imported as: from (...)stak import *
Or, in the usual way.
"""
from os import makedirs
from os.path import isdir, exists
from shutil import rmtree
from time import time

from .block0_typing import *
from .block1_commonData import appendToLog, stakFlags, log, traceLog, eventCnt, eventLabels, stdLogFiles
from .block2_pathOps import pathDirPrimi, pathDirVari, pathDirPrint
from .block4_creatingMroCallChains import jointLinksCallChain, splitLinksCallChain
from .block5_autoLocals import data as _data, linksAndFirstFrameLocalsFromFrame, splitLinkToStr
from .block7_compression import compressLinksGen
from .block8_parsingStdLogs import parseStdLogs
from .block9_savingAllLogs import saveAll, preProcessLog, strLinkCallChain, mroLinkToStrLink, saveStakLogToPrimitives, saveTraceLogToPrimitives, saveCompressedStakLogToVariants, saveStdLogsToPrimitives, saveSplicedToVariants, saveCompressedSplicedLogs


# Call-from-code interface
def omropocs():
    print ' <- '.join(jointLinksCallChain())

def omrolocs(silence=False):  # type: (bool) -> None
    """ Optional Method Resolution Order Logger Optional Call Stack """
    if silence: return
    appendToLog(
        (
            time(),
            stakFlags[0],
            tuple(splitLinksCallChain()),
        )
    )

def data(pretty=False, **dataForLogging):  # type: (bool, Any) -> None
    """ Log data structures, their callable & definer class names """

    strLink = next(jointLinksCallChain())
    _data(pretty, strLink, **dataForLogging)

def omrolocsalad(silence=False, pretty=False, **additionalDataForLogging):  # type: (bool, bool, Any) -> None
    """ Optional Method Resolution Order Logger Optional Call Stack And Locals Auto Data """
    if silence: return

    linksAndFirstFrameLocalsGen = linksAndFirstFrameLocalsFromFrame()
    firstFrameLocals = next(linksAndFirstFrameLocalsGen)  # type: Dic[str, Any]

    for key, value in firstFrameLocals.items():
        if key != 'self' and key != 'cls':
            additionalDataForLogging[key] = value

    splitLinks = tuple(linksAndFirstFrameLocalsGen)
    firstLinkAsStr = splitLinkToStr(splitLinks[0])

    appendToLog(
        (
            time(),
            stakFlags[0],
            splitLinks,
        )
    )

    _data(
        pretty,
        firstLinkAsStr,
        **additionalDataForLogging
    )

def autoLocals(silence=False, pretty=False, **additionalDataForLogging):  # type: (bool, bool, Any) -> None
    """ Logs locals from frame from which this method was called, optionally other kwargs """
    if silence: return

    linksAndFirstFrameLocalsGen = linksAndFirstFrameLocalsFromFrame()
    firstFrameLocals = next(linksAndFirstFrameLocalsGen)  # type: Dic[str, Any]

    for key, value in firstFrameLocals.items():
        if key != 'self' and key != 'cls':
            additionalDataForLogging[key] = value

    firstLinkAsStr = splitLinkToStr(next(linksAndFirstFrameLocalsGen))
    _data(
        pretty,
        firstLinkAsStr,
        **additionalDataForLogging
    )

def setTrace():
    raise NotImplementedError()

def delTrace():
    raise NotImplementedError()


# Call-from-shell interface
def save():
    """ Save stak.log, spliced, trimmed & more """

    # Make paths if don't exist just in time bc on innit might cause collisions (Yeah wtf, but I'm not messing with this)
    if not isdir(next(pathDirPrimi())):
        makedirs(next(pathDirPrimi()))
    if not isdir(next(pathDirVari())):
        makedirs(next(pathDirVari()))

    preprocessedLog = tuple(preProcessLog()
    )  # type: Tup[Tup[float, str, Uni[str, Tup[Uni[Tup[str, str], Tup[Lst[str], str]], ...]]], ...]

    # partStrLinkCallChains = tuple(self.__strLinkCallChainGen(log, self.__partStrLinkCreator))

    fullStrLinkCallChains = tuple(
        strLinkCallChain(
            preprocessedLog, mroLinkToStrLink
        )
    )  # type: Tup[Tup[Str4, str, Uni[Tup[str, ...], str]], ...]

    saveStakLogToPrimitives(fullStrLinkCallChains)

    # saveTraceLogToPrimitives(traceLog)

    callChainsWithCompressedStrLinks = tuple(compressLinksGen(fullStrLinkCallChains))
    saveCompressedStakLogToVariants(callChainsWithCompressedStrLinks)

    # Flags not padded yet
    parsedStdLogs = tuple(parseStdLogs())  # type: Tup[Tup[Tup[Str4, str, str], ...], ...]

    saveStdLogsToPrimitives(*parsedStdLogs)
    splicedLogs = saveSplicedToVariants(parsedStdLogs, callChainsWithCompressedStrLinks)

    saveCompressedSplicedLogs(splicedLogs)

def label(label=None):  # type: (Opt[str]) -> None
    """ Make a log entry with the passed label, else, with next label in eventLabels, if any, else print no-name label """
    global eventCnt

    if label is None:
        if eventCnt < len(eventLabels):
            label = eventLabels[eventCnt]
            eventCnt += 1
        else:
            label = 'NO-NAME LABEL' + str(len(eventLabels) - eventCnt)

    appendToLog(
        (
            time(),
            stakFlags[3],
            '\n========================================================= {} '
            '=========================================================\n\n'.format(label)
        )
    )

def clear():  # type: () -> None
    """ DANGER: Clears current logs, stak & std. Resets eventCnt (label print count) & more """
    for logPath in stdLogFiles:
        with open(logPath, 'w'): pass

    global eventCnt; eventCnt = 0
    log[:] = []
    _dateEntry()

def rmPrint():  # type: () -> None
    """ MUCH DANGER: Remove current print dir & all its logs """
    if exists(next(pathDirPrint())):
        rmtree(next(pathDirPrint()))

# Call-from-self autoface
def _dateEntry():
    # Since normal entries only log time, this one is used to log date, normally on logging session init
    appendToLog((time(), stakFlags[1], datetime.now().strftime('%Y-%m-%d\n')))


## Aliases
s = save
l = label
rp = rmp = rmPrint
c = clear


__all__ = (
    # Call from shell
    's', 'save',
    'l', 'label',
    'rp', 'rmp', 'rmPrint',
    'c', 'clear',

    # Call from code
    'omropocs',
    'omrolocs',
    'omrolocsalad',
    'data',
    'autoLocals',
    'setTrace',
    'delTrace',
)

