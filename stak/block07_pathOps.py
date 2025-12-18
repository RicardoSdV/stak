from .block00_autoImports import *

def makePathUnique(path):  # type: (str) -> str
    superPath = osPathDirName(path)
    nameToBeUnique, ext = osPathSplitExt(osPathBaseName(path))  # ext == '' when path is dir

    cnt = 0
    while osPathExists(path):
        cnt += 1
        path = osPathJoin(superPath, nameToBeUnique + str(cnt) + ext)
    return path

def getPrintDirPath():  # type: () -> str
    return osPathJoin(rootDir, taskDir, printDir)

def makePrintDirPath():  # type: () -> str
    return makePathUnique(getPrintDirPath())

def getPrimiDirPath():  # type: () -> str
    return osPathJoin(getPrintDirPath(), primiDir)

def getVariDirPath():  # type: () -> str
    return osPathJoin(getPrintDirPath(), variDir)

def getPickleDirPath():
    return osPathJoin(getPrintDirPath(), pickleDir)

def makeDirPaths():  # type: () -> None
    # todo: Only make dirs if there is logs to save.
    if not osPathIsDir(getPrimiDirPath()) and savePrimis           : osMakeDirs(getPrimiDirPath())
    if not osPathIsDir(getVariDirPath())  and saveVaris            : osMakeDirs(getVariDirPath())
    if not osPathIsDir(getPrintDirPath()) and saveStdStakSpliceComp: osMakeDirs(getPrintDirPath())
    if not osPathIsDir(getPickleDirPath())                         : osMakeDirs(getPickleDirPath())

def addSuffix(logName, suffix):  # type: (str, str) -> str
    name, ext = osPathSplitExt(logName)
    return name + suffix + ext

def removePrintDir():  # type: () -> None
    """ MUCH DANGER: Remove current print dir & all its logs """
    path = getPrintDirPath()
    if not osPathExists(path):
        E('Path = %s does not exist', path)
        return

    if bool(input('Are you sure of deleting: %s ?' % path)):
        shutilRmTree(path)

# Stak log paths
# -------------------------------------------------------------------------------------------------
def getPrimiStakPath():  # type: () -> str
    return makePathUnique(
        osPathJoin(getPrimiDirPath(), stakLogPrefix + primiSuffix + logExt)
    )

def getCompStakPath():  # type: () -> str
    return makePathUnique(
        osPathJoin(getVariDirPath(), stakLogPrefix + compSuffix + logExt)
    )
# -------------------------------------------------------------------------------------------------

# Trace log paths
# -------------------------------------------------------------------------------------------------
def getTracePath():  # type: () -> str
    return makePathUnique(
        osPathJoin(getPrimiDirPath(), traceLogPrefix + primiSuffix + logExt)
    )

def getCompactTracePath():  # type: () -> str
    return makePathUnique(
        osPathJoin(getVariDirPath(), traceLogPrefix + compactSuffix + logExt)
    )
# -------------------------------------------------------------------------------------------------

# Long term storage paths
# -------------------------------------------------------------------------------------------------
def getPicklePath():  # type: () -> str
    return makePathUnique(
        osPathJoin(getPickleDirPath(), picklePrefix + pickleExt)
    )
# -------------------------------------------------------------------------------------------------

# In house intern of paths.  # TODO: Make paths unique in logs.
# -------------------------------------------------------------------------------------------------
# pathsByIds = {}
# idsByPaths = {}
# pathIdCnt  = Cnt()
#
# def getIdFromPath(path):
#     path = intern(path)
#     if path in idsByPaths:
#         return idsByPaths[path]
#
#     ID = pathIdCnt.cnt
#     pathsByIds[ID] = path
#     idsByPaths[path] = ID
#     pathIdCnt.cnt += 1
#
#     return ID
# -------------------------------------------------------------------------------------------------

def isIgnorePath(path):  # type: (str) -> bool
    return (
        path[:lenOsAbsPath] != osAbsPath and
        path[:lenAbsPackagePath] != absPackagePath
    )

def getAbsPathForBlockName(name):  # type: (str) -> str
    return __unitedModPaths__[__unitedModNames__.index(name)]
