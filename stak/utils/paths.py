from .log import ERROR
from ..lib import (
    osPathDirName, osPathAbsPath, osPathSplitExt, osPathBaseName, osPathExists, osPathJoin, osPathIsDir, osMakeDirs,
    shutilRmTree, lenOsAbsPath, osAbsPath, sysGetFrame)
from ..state import config

# Paths
absPackagePath      = osPathDirName(osPathAbsPath(__file__))  # stak/stak
lenAbsPackagePath   = len(absPackagePath)
splitPackageDotPath = __name__.split('.')[:-1]
packageDotPath      = '.'.join(splitPackageDotPath)
lenPackageDotPath   = len(packageDotPath)

# os does not hold the correct path char for certain programs, when inspecting frames,
# for os file ops should os.path.join, but for frame ops use pathSplitChar.
pathSplitChar = '/' if '/' in sysGetFrame(0).f_code.co_filename else '\\'


def makePathUnique(path):  # type: (str) -> str
    superPath = osPathDirName(path)
    nameToBeUnique, ext = osPathSplitExt(osPathBaseName(path))  # ext == '' when path is dir

    cnt = 0
    while osPathExists(path):
        cnt += 1
        path = osPathJoin(superPath, nameToBeUnique + str(cnt) + ext)
    return path

def getPrintDirPath():  # type: () -> str
    return osPathJoin(config['rootDir'], config['taskDir'], config['printDir'])

def makePrintDirPath():  # type: () -> str
    return makePathUnique(getPrintDirPath())

def getPrimiDirPath():  # type: () -> str
    return osPathJoin(getPrintDirPath(), config['primiDir'])

def getVariDirPath():  # type: () -> str
    return osPathJoin(getPrintDirPath(), config['variDir'])

def getPickleDirPath():
    return osPathJoin(getPrintDirPath(), config['pickleDir'])

def makeDirPaths():  # type: () -> None
    # todo: Only make dirs if there is logs to save.
    if not osPathIsDir(getPrimiDirPath()) and config['savePrimis']           : osMakeDirs(getPrimiDirPath())
    if not osPathIsDir(getVariDirPath())  and config['saveVaris']            : osMakeDirs(getVariDirPath())
    if not osPathIsDir(getPrintDirPath()) and config['saveStdStakSpliceComp']: osMakeDirs(getPrintDirPath())
    if not osPathIsDir(getPickleDirPath())                                   : osMakeDirs(getPickleDirPath())

def addSuffix(logName, suffix):  # type: (str, str) -> str
    name, ext = osPathSplitExt(logName)
    return name + suffix + ext

def removePrintDir():  # type: () -> None
    """ MUCH DANGER: Remove current print dir & all its logs """
    path = getPrintDirPath()
    if not osPathExists(path):
        ERROR('Path = %s does not exist', path)
        return

    if bool(input('Are you sure of deleting: %s ?' % path)):
        shutilRmTree(path)

# Stak log paths
# -------------------------------------------------------------------------------------------------
def getPrimiStakPath():  # type: () -> str
    return makePathUnique(
        osPathJoin(getPrimiDirPath(), config['stakLogPrefix'] + config['primiSuffix'] + config['logExt'])
    )

def getCompStakPath():  # type: () -> str
    return makePathUnique(
        osPathJoin(getVariDirPath(), config['stakLogPrefix'] + config['compSuffix'] + config['logExt'])
    )
# -------------------------------------------------------------------------------------------------

# Trace log paths
# -------------------------------------------------------------------------------------------------
def getTracePath():  # type: () -> str
    return makePathUnique(
        osPathJoin(getPrimiDirPath(), config['traceLogPrefix'] + config['primiSuffix'] + config['logExt'])
    )

def getCompactTracePath():  # type: () -> str
    return makePathUnique(
        osPathJoin(getVariDirPath(), config['traceLogPrefix'] + config['compactSuffix'] + config['logExt'])
    )
# -------------------------------------------------------------------------------------------------

# Long term storage paths
# -------------------------------------------------------------------------------------------------
def getPicklePath():  # type: () -> str
    return makePathUnique(
        osPathJoin(getPickleDirPath(), config['picklePrefix'] + config['pickleExt'])
    )
# -------------------------------------------------------------------------------------------------


def isIgnorePath(path):  # type: (str) -> bool
    return (
        path[:lenOsAbsPath] != osAbsPath and
        path[:lenAbsPackagePath] != absPackagePath
    )
