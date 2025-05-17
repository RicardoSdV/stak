from itertools import chain
from os import makedirs, walk, __file__ as osPath
from os.path import join, isdir, splitext, exists, basename, dirname, isfile
from shutil import rmtree
from sys import _getframe

from .block00_typing import *
from .block02_settingObj import so
from .block03_constants import logFilesExt, jsonFilesExt, zippedFilesExt
from .z_utils import E

# os does not hold the correct path for certain programs, when inspecting frames
# specifically, for saving to disk should still use os.path.join, but for frame ops
# must use experimentally determined pathSplitChar.
pathSplitChar = '/' if '/' in _getframe(0).f_code.co_filename else '\\'

splitFilePath = __file__.split(pathSplitChar)
splitPackagePath = splitFilePath[0: -1]
packagePath = pathSplitChar.join(splitPackagePath)

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
        E('Path = %s does not exist', path)
        return

    if bool(input('Are you sure of deleting: %s ?' % path)):
        rmtree(path)

def makeFilePathUnique(path):  # type: (str) -> str
    # Increment an integer suffix until path of file (not dir) is unique
    fileName, ext = splitext(basename(path))
    dirPath = dirname(path)

    cnt = 0
    while isfile(path):
        cnt += 1
        path = join(dirPath, fileName + str(cnt) + ext)
    return path

# Stak log paths
# -------------------------------------------------------------------------------------------------
def getPrimiStakPath():  # type: () -> str
    return makeFilePathUnique(
        join(getPrimiDirPath(), so.stakLogPrefix + so.primiSuffix + logFilesExt)
    )

def getCompStakPath():  # type: () -> str
    return makeFilePathUnique(
        join(getVariDirPath(), so.stakLogPrefix + so.compSuffix + logFilesExt)
    )
# -------------------------------------------------------------------------------------------------

# Trace log paths
# -------------------------------------------------------------------------------------------------
def getTracePath():  # type: () -> str
    return makeFilePathUnique(
        join(getPrimiDirPath(), so.traceLogPrefix + so.primiSuffix + logFilesExt)
    )

def getCompactTracePath():  # type: () -> str
    return makeFilePathUnique(
        join(getVariDirPath(), so.traceLogPrefix + so.compactSuffix + logFilesExt)
    )
# -------------------------------------------------------------------------------------------------

# Standard log paths
# -------------------------------------------------------------------------------------------------
def getStdLogPath(prefix):  # type: (str) -> str
    return join(so.stdDir, prefix + logFilesExt)

def getPrimiStdPath(prefix):  # type: (str) -> str
    return makeFilePathUnique(
        join(getPrimiDirPath(), prefix + so.primiSuffix + logFilesExt)
    )
# -------------------------------------------------------------------------------------------------

# Splice paths
# -------------------------------------------------------------------------------------------------
def getStdStakSplicePath(prefix):  # type: (str) -> str
    return makeFilePathUnique(
        join(getVariDirPath(), prefix + so.stdStakSpliceSuffix + logFilesExt)
    )

def getCompStdStakSplicePath(prefix):  # type: (str) -> str
    return makeFilePathUnique(
        join(getPrintDirPath(), prefix + so.compStdStakSpliceSuffix + logFilesExt)
    )
# -------------------------------------------------------------------------------------------------

# Json paths
# -------------------------------------------------------------------------------------------------
def getJsonPath():  # type: () -> str
    return makeFilePathUnique(
        join(getJsonDirPath(), so.jsonPrefix + jsonFilesExt)
    )

def getZippedPath():  # type: () -> str
    return makeFilePathUnique(
        join(getJsonDirPath(), so.zippedPrefix + zippedFilesExt)
    )
# -------------------------------------------------------------------------------------------------

# Path Ignore
# -------------------------------------------------------------------------------------------------
def walkDirForSuffix(dirPath, suffix='.py'):  # type: (str, str) -> Itrt[str]
    return (
        root + pathSplitChar + file
        for root, dirs, files in walk(dirPath)
        for file in files
        if file.endswith(suffix)
    )

# TODO: This should be injected, but since the paths are absolute it needs to be recomputed every
#  time the location of stak changes, so to make this happen the injection logic needs to be changed
#  the injectors need to be moved inside the package, and they need to be ran on location change.
pathsIgnoredOnLogGather = set(
    chain(
        walkDirForSuffix(dirname(osPath)),
        walkDirForSuffix(packagePath),
    )
)
pathsIgnoredOnLogGather.add('<console>')

# -------------------------------------------------------------------------------------------------
