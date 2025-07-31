from os      import makedirs
from os.path import basename, dirname, exists, isdir, join, splitext
from shutil  import rmtree

from .block00_typing        import *
from .block02_settingObj    import so
from . import block03_constants as cs
from .block16_utils         import E, Cnt


splitFilePath = __file__.split(cs.pathSplitChar)
splitPackagePath = splitFilePath[0: -1]
packagePath = cs.pathSplitChar.join(splitPackagePath)

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
def getPrimiStakPath(logExt=cs.logExt):  # type: (str) -> str
    return makePathUnique(
        join(getPrimiDirPath(), so.stakLogPrefix + so.primiSuffix + logExt)
    )

def getCompStakPath(logExt=cs.logExt):  # type: (str) -> str
    return makePathUnique(
        join(getVariDirPath(), so.stakLogPrefix + so.compSuffix + logExt)
    )
# -------------------------------------------------------------------------------------------------

# Trace log paths
# -------------------------------------------------------------------------------------------------
def getTracePath(logExt=cs.logExt):  # type: (str) -> str
    return makePathUnique(
        join(getPrimiDirPath(), so.traceLogPrefix + so.primiSuffix + logExt)
    )

def getCompactTracePath(logExt=cs.logExt):  # type: (str) -> str
    return makePathUnique(
        join(getVariDirPath(), so.traceLogPrefix + so.compactSuffix + logExt)
    )
# -------------------------------------------------------------------------------------------------

# Standard log paths
# -------------------------------------------------------------------------------------------------
def getStdLogPath(prefix, logExt=cs.logExt):  # type: (str, str) -> str
    return join(so.stdDir, prefix + logExt)

def getPrimiStdPath(prefix, logExt=cs.logExt):  # type: (str, str) -> str
    return makePathUnique(
        join(getPrimiDirPath(), prefix + so.primiSuffix + logExt)
    )
# -------------------------------------------------------------------------------------------------

# Splice paths
# -------------------------------------------------------------------------------------------------
def getStdStakSplicePath(prefix, logExt=cs.logExt):  # type: (str, str) -> str
    return makePathUnique(
        join(getVariDirPath(), prefix + so.stdStakSpliceSuffix + logExt)
    )

def getCompStdStakSplicePath(prefix, logExt=cs.logExt):  # type: (str, str) -> str
    return makePathUnique(
        join(getPrintDirPath(), prefix + so.compStdStakSpliceSuffix + logExt)
    )
# -------------------------------------------------------------------------------------------------

# Long term storage paths
# -------------------------------------------------------------------------------------------------
def getPicklePath(pickleExt=cs.pickleExt):  # type: (str) -> str
    return makePathUnique(
        join(getPickleDirPath(), so.picklePrefix + pickleExt)
    )
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
