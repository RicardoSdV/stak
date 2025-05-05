from os import makedirs
from os.path import join, isdir, splitext, exists, basename, dirname, isfile
from shutil import rmtree
from sys import _getframe

from .block00_typing import *
from .block02_settingObj import so
from .block03_constants import logFilesExt, jsonFilesExt
from .z_utils import redStr


pathSplitChar = '/' if '/' in _getframe(0).f_code.co_filename else '\\'

def getPrintDirPath():  # type: () -> str
    return join(so.rootDir, so.taskDir, so.printDir)

def getPrimiDirPath():  # type: () -> str
    return join(getPrintDirPath(), so.primiDir)

def getVariDirPath():  # type: () -> str
    return join(getPrintDirPath(), so.variDir)

def getJsonDirPath():
    return join(getPrintDirPath(), so.jsonDir)

def makeDirPaths():  # type: () -> None
    # todo: Only make dirs if there is logs to save.
    if not isdir(getPrimiDirPath()) and so.savePrimis    : makedirs(getPrimiDirPath())
    if not isdir(getVariDirPath())  and so.saveVaris     : makedirs(getVariDirPath())
    if not isdir(getPrintDirPath()) and so.saveCompSplice: makedirs(getPrintDirPath())
    if not isdir(getJsonDirPath()): makedirs(getJsonDirPath())

def addSuffix(logName, suffix):  # type: (str, str) -> str
    name, ext = splitext(logName)
    return name + suffix + ext

def removePrintDir():  # type: () -> None
    """ MUCH DANGER: Remove current print dir & all its logs """
    path = getPrintDirPath()
    if not exists(path):
        print redStr('ERROR: Path = %s does not exist', path)
        return

    if bool(input('Are you sure of deleting: %s ?' % path)):
        rmtree(path)

def getStdLogPaths():  # type: () -> Itrt[str]
    for prefix in so.stdLogPrefixes:
        yield join(so.stdDir, prefix + logFilesExt)

def makeFilePathUnique(path):  # type: (str) -> str
    # Increment an integer suffix until path of file (not dir) is unique
    fileName, ext = splitext(basename(path))
    dirPath = dirname(path)

    cnt = 0
    while isfile(path):
        cnt += 1
        path = join(dirPath, fileName + str(cnt) + ext)
    return path

def getPrimiStakPaths():  # type: () -> Tup[str]
    return makeFilePathUnique(
        join(getPrimiDirPath(), so.stakLogPrefix + so.primiSuffix + logFilesExt)
    ),

def getPrimiStdPaths():  # type: () -> Itrt[str]
    for prefix in so.stdLogPrefixes:
        yield makeFilePathUnique(
            join(getPrimiDirPath(), prefix + so.primiSuffix + logFilesExt)
        )

def getCompStakPaths():  # type: () -> Tup[str]
    return makeFilePathUnique(
        join(getVariDirPath(), so.stakLogPrefix + so.compSuffix + logFilesExt)
    ),

def getStdStakSplicePaths():  # type: () -> Itrt[str]
    for prefix in so.stdLogPrefixes:
        yield makeFilePathUnique(
            join(getVariDirPath(), prefix + so.stdStakSpliceSuffix + logFilesExt)
        )

def getCompStdStakSplicePaths():  # type: () -> Itrt[str]
    for prefix in so.stdLogPrefixes:
        yield makeFilePathUnique(
            join(getPrintDirPath(), prefix + so.compStdStakSpliceSuffix + logFilesExt)
        )

def getTracePaths():  # type: () -> Tup[str]
    return makeFilePathUnique(
        join(getPrimiDirPath(), so.traceLogPrefix + so.primiSuffix + logFilesExt)
    ),

def getCompactTracePaths():  # type: () -> Tup[str]
    return makeFilePathUnique(
        join(getVariDirPath(), so.traceLogPrefix + so.compactSuffix + logFilesExt)
    ),

def getJsonPath():  # type: () -> str
    return makeFilePathUnique(
        join(getJsonDirPath(), so.stakLogPrefix + jsonFilesExt)
    )
