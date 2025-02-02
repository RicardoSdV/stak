from functools import partial
from os import makedirs
from os.path import join, isdir, splitext, exists, basename, dirname, isfile
from shutil import rmtree
from sys import _getframe

from .block00_typing import *
from .block01_settings import rootDir, taskDir, printDir, primiDir, variDir, stdLogPrefixes, stdDir, logFilesExt, stakLogPrefix, primiSuffix, compSuffix, stdStakSpliceSuffix, compStdStakSpliceSuffix, traceLogPrefix, compactSuffix


pathSplitChar = '/' if '/' in _getframe(0).f_code.co_filename else '\\'

# Dynamic path generators
getPrintDirPath = partial(join, rootDir, taskDir, printDir)

def getPrimiDirPath():  # type: () -> str
    return join(getPrintDirPath(), primiDir)

def getVariDirPath():  # type: () -> str
    return join(getPrintDirPath(), variDir)

def makeDirPaths():
    if not isdir(getPrimiDirPath()): makedirs(getPrimiDirPath())
    if not isdir(getVariDirPath()) : makedirs(getVariDirPath())

def addSuffix(logName, suffix):  # type: (str, str) -> str
    name, ext = splitext(logName)
    return name + suffix + ext

def removePrintDir():  # type: () -> None
    """ MUCH DANGER: Remove current print dir & all its logs """
    if exists(getPrintDirPath()): rmtree(getPrintDirPath())

def getStdLogPaths():  # type: () -> Itrt[str]
    for prefix in stdLogPrefixes:
        yield join(stdDir, prefix + logFilesExt)

def makeFilePathUnique(path):  # type: (str) -> str
    # Increment an integer suffix until path of file (not dir) is unique
    fileName, ext = splitext(basename(path))
    dirPath = dirname(path)

    cnt = 0
    while isfile(path):
        cnt += 1
        path = join(dirPath, fileName + str(cnt) + ext)
    return path

def genPrimiStakPaths():
    while True:
        yield makeFilePathUnique(
            join(getPrimiDirPath(), stakLogPrefix + primiSuffix + logFilesExt)
        )

def genPrimiStdPaths():
    while True:
        for prefix in stdLogPrefixes:
            yield makeFilePathUnique(
                join(getPrimiDirPath(), prefix + primiSuffix + logFilesExt)
            )

def genCompStakPaths():
    while True:
        yield makeFilePathUnique(
            join(getVariDirPath(), stakLogPrefix + compSuffix + logFilesExt)
        )

def genStdStakSplicePaths():
    while True:
        for prefix in stdLogPrefixes:
            yield makeFilePathUnique(
                join(getVariDirPath(), prefix + stdStakSpliceSuffix + logFilesExt)
            )

def genCompStdStakSplicePaths():
    while True:
        for prefix in stdLogPrefixes:
            yield makeFilePathUnique(
                join(getPrintDirPath(), prefix + compStdStakSpliceSuffix + logFilesExt)
            )

def genTracePaths():
    while True:
        yield makeFilePathUnique(
            join(getPrimiDirPath(), traceLogPrefix + primiSuffix + logFilesExt)
        )

def genCompactTracePaths():
    while True:
        yield makeFilePathUnique(
            join(getVariDirPath(), traceLogPrefix + compactSuffix + logFilesExt)
        )

genPrimiStakPaths         = genPrimiStakPaths()
genPrimiStdPaths          = genPrimiStdPaths()
genCompStakPaths          = genCompStakPaths()
genStdStakSplicePaths     = genStdStakSplicePaths()
genCompStdStakSplicePaths = genCompStdStakSplicePaths()
genTracePaths             = genTracePaths()
genCompactTracePaths      = genCompactTracePaths()

def getPackageName():
    return __name__.split('.')[-2]
