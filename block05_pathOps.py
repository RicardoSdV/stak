from itertools import chain
from os        import makedirs, walk, __file__ as osPath
from os.path   import basename, dirname, exists, isdir, join, splitext
from shutil    import rmtree
from sys       import _getframe

from .block00_typing     import *
from .block02_settingObj import so
from .block03_constants  import logFilesExt, pickleFilesExt
from .z_utils import E, Cnt, timeCall

# os does not hold the correct path for certain programs, when inspecting frames
# specifically, for saving to disk should still use os.path.join, but for frame ops
# must use experimentally determined pathSplitChar.
pathSplitChar = '/' if '/' in _getframe(0).f_code.co_filename else '\\'

splitFilePath = __file__.split(pathSplitChar)
splitPackagePath = splitFilePath[0: -1]
packagePath = pathSplitChar.join(splitPackagePath)

def makePathUnique(path):  # type: (str) -> str
    superPath = dirname(path)
    nameToBeUnique, ext = splitext(basename(path))  # ext == '' when path is dir

    cnt = 0
    while exists(path):
        cnt += 1
        path = join(superPath, nameToBeUnique + str(cnt) + ext)
    return path

def getPrintDirPath():  # type: () -> str
    return join(so.rootDir, so.taskDir, so.printDir)

def makePrintDirPath():  # type: () -> str
    return makePathUnique(getPrintDirPath())

def getPrimiDirPath():  # type: () -> str
    return join(getPrintDirPath(), so.primiDir)

def getVariDirPath():  # type: () -> str
    return join(getPrintDirPath(), so.variDir)

def getPickleDirPath():
    return join(getPrintDirPath(), so.pickleDir)

def makeDirPaths():  # type: () -> None
    # todo: Only make dirs if there is logs to save.
    if not isdir(getPrimiDirPath()) and so.savePrimis    : makedirs(getPrimiDirPath())
    if not isdir(getVariDirPath())  and so.saveVaris     : makedirs(getVariDirPath())
    if not isdir(getPrintDirPath()) and so.saveCompSplice: makedirs(getPrintDirPath())
    if not isdir(getPickleDirPath()): makedirs(getPickleDirPath())

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

# Stak log paths
# -------------------------------------------------------------------------------------------------
def getPrimiStakPath():  # type: () -> str
    return makePathUnique(
        join(getPrimiDirPath(), so.stakLogPrefix + so.primiSuffix + logFilesExt)
    )

def getCompStakPath():  # type: () -> str
    return makePathUnique(
        join(getVariDirPath(), so.stakLogPrefix + so.compSuffix + logFilesExt)
    )
# -------------------------------------------------------------------------------------------------

# Trace log paths
# -------------------------------------------------------------------------------------------------
def getTracePath():  # type: () -> str
    return makePathUnique(
        join(getPrimiDirPath(), so.traceLogPrefix + so.primiSuffix + logFilesExt)
    )

def getCompactTracePath():  # type: () -> str
    return makePathUnique(
        join(getVariDirPath(), so.traceLogPrefix + so.compactSuffix + logFilesExt)
    )
# -------------------------------------------------------------------------------------------------

# Standard log paths
# -------------------------------------------------------------------------------------------------
def getStdLogPath(prefix):  # type: (str) -> str
    return join(so.stdDir, prefix + logFilesExt)

def getPrimiStdPath(prefix):  # type: (str) -> str
    return makePathUnique(
        join(getPrimiDirPath(), prefix + so.primiSuffix + logFilesExt)
    )
# -------------------------------------------------------------------------------------------------

# Splice paths
# -------------------------------------------------------------------------------------------------
def getStdStakSplicePath(prefix):  # type: (str) -> str
    return makePathUnique(
        join(getVariDirPath(), prefix + so.stdStakSpliceSuffix + logFilesExt)
    )

def getCompStdStakSplicePath(prefix):  # type: (str) -> str
    return makePathUnique(
        join(getPrintDirPath(), prefix + so.compStdStakSpliceSuffix + logFilesExt)
    )
# -------------------------------------------------------------------------------------------------

# Long term storage paths
# -------------------------------------------------------------------------------------------------
def getPicklePath():  # type: () -> str
    return makePathUnique(
        join(getPickleDirPath(), so.picklePrefix + pickleFilesExt)
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

@timeCall  # TODO: This is the bottleneck for importing speed
def getBaseIgnoredPaths():
    return set(
        chain(
            walkDirForSuffix(dirname(osPath)),
            walkDirForSuffix(packagePath),
            ('<console>', '<string>'),
        )
    )

pathsIgnoredOnLogGather = getBaseIgnoredPaths()

# -------------------------------------------------------------------------------------------------

# In house intern of paths.
# -------------------------------------------------------------------------------------------------
pathsByIds = {}
idsByPaths = {}
pathIdCnt  = Cnt()

def getIdFromPath(path, pathsByIds=pathsByIds, idsByPaths=idsByPaths, pathIdCnt=pathIdCnt):
    path = intern(path)
    if path in idsByPaths:
        return idsByPaths[path]

    ID = pathIdCnt.cnt
    pathsByIds[ID] = path
    idsByPaths[path] = ID
    pathIdCnt.cnt += 1

    return ID
# -------------------------------------------------------------------------------------------------
