"""
Some stuff is more convenient if computed, but really it only needs to be computed once, not every time the program is run.
So, the solution is to compute these things in this file & inject the results into stak.
Also, removes some clutter from the code.
Also, settings are injected by running this.

Since blocks are numbered it is very tedious to insert or delete a new block,
running this file will rename the appropriate files when one of them is deleted
& insert & rename when "newBlockName" is provided automatically.
"""
import sys

from collections import defaultdict
from itertools   import chain, izip

from .block00_typing        import *
from . import block01_settings   as settings
from . import block02_settingObj as settingObj
from . import block03_constants  as cs
from .block16_utils          import read, write

## Block prefix
newBlockPrefix    = 'block'
oldBlockPrefix    = cs.blockPrefix
lenNewBlockPrefix = len(newBlockPrefix)
lenOldBlockPrefix = len(oldBlockPrefix)

osPath   = os.path
abspath  = osPath.abspath
joinPath = osPath.join

## Old & new paths
dirname        = osPath.dirname
oldOsPath      = cs.osPath
newOsPath      = dirname(os.__file__)
oldPackagePath = cs.packagePath
newPackagePath = dirname(abspath(__file__))
constsPath     = abspath(cs.__file__)

oldPathSplitChar = '/' if '/' in sys._getframe(0).f_code.co_filename else '\\'
newPathSplitChar = cs.pathSplitChar

pyExt     = cs.pyExt
nLenPyExt = -cs.lenPyCompExt

def replaceInPlace(lines, lookingFor, dataStructure):  # type: (Lst[str], str, Any) -> None
    for i, line in enumerate(lines):
        if line.startswith(lookingFor):
            lines[i] = lookingFor + str(dataStructure)
            return
    raise ValueError('Looking for "{}" prefix & not found!'.format(lookingFor))


## On blocks changed run block injection
# ---------------------------------------------------------------------------------------------------------------------
listDir = os.listdir
oldBlockNames = [
    name[nLenPyExt:]
    for name in listDir(newPackagePath)
    if name[nLenPyExt:] == pyExt and name != '__init__.py'
]
newBlockNames = cs.blockNames

if oldBlockNames != newBlockNames:

    ## Add / remove block names
    # -----------------------------------------------------------------------------------------------------------------
    oldBlockNamesSet = set(oldBlockNames); newBlockNamesSet = set(newBlockNames)

    blocksToRemove = oldBlockNamesSet - newBlockNamesSet
    blocksToAdd    = newBlockNamesSet - oldBlockNamesSet

    if blocksToRemove and blocksToAdd:
        print "[STAK] ERROR: Can't add & remove blocks at the same time"
        blocksToRemove = blocksToAdd = {}

    removeFile = os.remove
    for name in blocksToRemove:
        removeFile(joinPath(newPackagePath, name + pyExt))

    for name in blocksToAdd:
        write(
            joinPath(newPackagePath, name + pyExt),
            ('from .block00_typing import *\n',)
        )
    # -----------------------------------------------------------------------------------------------------------------

    ## Make new by old blocks
    # -----------------------------------------------------------------------------------------------------------------
    oldMaxBlockIdxLen = len(str(len(oldBlockNames) - 1))
    newMaxBlockIdxLen = len(str(len(newBlockNames) - 1))

    blockPrefix = cs.blockPrefix
    newByOldBlocks = []; append = newByOldBlocks.append
    enumOldBlockNames = list(enumerate(oldBlockNames))
    for newIdx, newName in enumerate(newBlockNames):
        for oldIdx, oldName in enumOldBlockNames:
            if oldName == newName:
                break
        else:
            continue

        oldIdxStr = str(newIdx).zfill(oldMaxBlockIdxLen)
        newIdxStr = str(oldIdx).zfill(newMaxBlockIdxLen)

        append(
            (
                blockPrefix + oldIdxStr + '_' + oldName,
                blockPrefix + newIdxStr + '_' + newName,
            )
        )
    # -----------------------------------------------------------------------------------------------------------------

    ## Rename block files.
    # -----------------------------------------------------------------------------------------------------------------
    renamePath = os.rename
    blockPaths = []; append = blockPaths.append
    for oldBlock, newBlock in newByOldBlocks:
        oldBlockPath = joinPath(newPackagePath, oldBlock + pyExt)
        newBlockPath = joinPath(newPackagePath, newBlock + pyExt)
        renamePath(oldBlockPath, newBlockPath)
        append(newBlockPath)
    # -----------------------------------------------------------------------------------------------------------------

    ## Rename references to blocks, sortBlock imports.
    # -----------------------------------------------------------------------------------------------------------------
    for path in blockPaths:
        lines = read(path)

        importsStarted = importsFinished = False
        imports = []; appImports = imports.append
        lineNos = []; appLineNos = lineNos.append

        for i, line in enumerate(lines):

            anyBlockInLine = False
            for oldBlock, newBlock in newByOldBlocks:
                if oldBlock in line:
                    line = line.replace(oldBlock, newBlock)
                    lines[i] = line
                    anyBlockInLine = True

            if importsFinished:
                continue

            if anyBlockInLine and ' import ' in line:
                importsStarted = True
                appImports(line)
                appLineNos(i)

            elif importsStarted:
                importsFinished = True

        if importsStarted and importsFinished:
            imports.sort()
            for num, _import in izip(lineNos, imports):
                lines[num] = _import
        elif not importsStarted and not importsFinished:
            continue
        else:
            print '[STAK] ERROR: Imports sorting. started', importsStarted, 'finished', importsFinished
# ---------------------------------------------------------------------------------------------------------------------


## Injection on paths changed
# ---------------------------------------------------------------------------------------------------------------------
if (
        oldOsPath != newOsPath or
        oldPackagePath != newPackagePath
):
    ## Make ignored paths
    # -----------------------------------------------------------------------------------------------------------------
    walk = os.walk
    pathsIgnore = ['<console>', '<string>']
    append = pathsIgnore.append
    for path in (newOsPath, newPackagePath):
        for root, dirs, files in walk(path):
            root += newPathSplitChar
            for _file in files:
                if _file[nLenPyExt:] == pyExt:
                    append(root + _file)
    # -----------------------------------------------------------------------------------------------------------------

    ## Inject lines in place
    # -----------------------------------------------------------------------------------------------------------------
    lines = read(constsPath)
    replaceInPlace(lines, 'osPath      = ', newOsPath)
    replaceInPlace(lines, 'packagePath = ', newPackagePath)
    replaceInPlace(lines, 'osPaths = ', '{' + str(set(pathsIgnore)).lstrip('set([').rstrip('])') + '}')
    write(constsPath, lines)
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

## Run manual injectors.
# ---------------------------------------------------------------------------------------------------------------------
if cs.runInjectors:
    # Settings injection
    # -----------------------------------------------------------------------------------------------------------------
    settingsPath   = settings.__file__
    settingObjPath = settingObj.__file__

    settingsLines   = read(settingsPath)
    settingObjLines = read(settingObjPath)

    settingsNames = [name for name in settings.__dict__ if name[-2:] != '__']

    replaceInPlace(settingObjLines, '    __slots__ = ', settingsNames)

    indentedLines = [
        ('        ' + ('self.' + line if ' = ' in line and any(name in line for name in settingsNames) else line))
        if line != '\n' else line
        for line in settingsLines
    ]
    indentedLines.reverse()

    i = -1
    started = finished = 0
    pop    = indentedLines.pop
    insert = settingObjLines.insert
    while indentedLines:
        i += 1
        objLine = settingObjLines[i]

        if started:
            newLine = pop()

            if objLine == '        ## Init finit (do not delete this comment)\n':
                finished = i - 1

            if finished:
                insert(finished, newLine)
            else:
                settingObjLines[i] = newLine

        elif objLine == '    def __init__(self):\n':
            started = 1

    write(settingObjPath, settingObjLines)
    # -----------------------------------------------------------------------------------------------------------------

    ## Constants injection
    # -----------------------------------------------------------------------------------------------------------------
    def padFlags(flags):  # type: (Seq[str]) -> Lst[str]
        maxFlagLen = max(len(flag) for flag in flags)
        return [': ' + flag + (' ' * (maxFlagLen - len(flag))) + ': ' for flag in flags]

    stdFlags = cs.stdFlags

    paddedStdFlags   = padFlags(stdFlags)
    paddedStakFlags  = padFlags(cs.stakFlags)
    paddedTraceFlags = padFlags(cs.traceFlags)
    padByNotStdFlags = {flag: pFlag for flag, pFlag in izip(stdFlags, paddedStdFlags)}

    allFlags = list(chain(cs.stakFlags, cs.stdFlags, (cs.cutoffFlag,)))
    pAllFlags = padFlags(allFlags)
    padByNotAllFlags =  {flag: pFlag for flag, pFlag in izip(allFlags, pAllFlags)}

    ## Make whole enough std flags
    repeatsByCutoffFlags = defaultdict(int)  # type: Dic[str, int]
    wholeByCutoffFlags = {}

    for wholeFlag in stdFlags:
        cutoffFlag = wholeFlag[1:]
        while cutoffFlag:
            repeatsByCutoffFlags[cutoffFlag] += 1
            wholeByCutoffFlags[cutoffFlag] = wholeFlag
            cutoffFlag = cutoffFlag[1:]

    wholeEnoughFlags = [
        (cutoffFlag, len(cutoffFlag), wholeByCutoffFlags[cutoffFlag])
        for cutoffFlag in sorted(repeatsByCutoffFlags, key=len, reverse=True)
        if repeatsByCutoffFlags[cutoffFlag] == 1
    ]

    ## Inject consts.
    constsLines = read(constsPath)

    replaceInPlace(constsLines, 'paddedStdFlags = '     , paddedStdFlags)
    replaceInPlace(constsLines, 'pStakFlags = '         , paddedStakFlags)
    replaceInPlace(constsLines, 'pTraceFlags = '        , paddedTraceFlags)
    replaceInPlace(constsLines, 'pStdFlagsByStdFlags = ', padByNotStdFlags)
    replaceInPlace(constsLines, 'allPflagsByFlags = '   , padByNotAllFlags)
    replaceInPlace(constsLines, 'wholeEnoughs = '       , wholeEnoughFlags)
    replaceInPlace(constsLines, 'runInjectors = '       , 0)

    write(constsPath, constsLines)
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


## Unload all blocks
# ---------------------------------------------------------------------------------------------------------------------
modules = sys.modules
packageDotPathPrefix = __name__.split('.')[:-1].join('.') + '.'
for name in newBlockNames:
    moduleDotPath = packageDotPathPrefix + name
    if moduleDotPath in modules:
        module = modules.pop(moduleDotPath)
        del module
# ---------------------------------------------------------------------------------------------------------------------
