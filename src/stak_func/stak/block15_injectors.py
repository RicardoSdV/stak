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
import os

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
dirname     = osPath.dirname
packagePath = dirname(abspath(__file__))
constsPath  = abspath(cs.__file__)

oldPathSplitChar = '/' if '/' in sys._getframe(0).f_code.co_filename else '\\'
newPathSplitChar = cs.pathSplitChar

pyExt     = cs.pyExt
nLenPyExt = -cs.lenPyExt

def replaceInPlace(lines, lookingFor, dataStructure):  # type: (Lst[str], str, Any) -> None
    for i, line in enumerate(lines):
        if line.startswith(lookingFor):
            lines[i] = '%s%r' % (lookingFor, dataStructure)
            return
    print '[STAK] ERROR: Looking for', lookingFor, 'prefix & not found'


## On blocks changed run block injection
# ---------------------------------------------------------------------------------------------------------------------
listDir = os.listdir
oldBlockFiles = [
    name[:nLenPyExt]
    for name in listDir(packagePath)
    if name[nLenPyExt:] == pyExt and name != '__init__.py'
]

oldBlockNames = [name.split('_')[-1] for name in oldBlockFiles]
newBlockNames = cs.blockNames

blockPrefix = cs.blockPrefix

if oldBlockNames != newBlockNames:
    oldMaxBlockIdxLen = len(str(len(oldBlockNames) - 1))
    newMaxBlockIdxLen = len(str(len(newBlockNames) - 1))

    newBlockFiles = [
        blockPrefix + str(i).zfill(newMaxBlockIdxLen) + '_' + name
        for i, name in enumerate(newBlockNames)
    ]

    ## Add / remove block names
    # -----------------------------------------------------------------------------------------------------------------
    oldBlockNamesSet = set(oldBlockNames)
    newBlockNamesSet = set(newBlockNames)

    blockNamesToRemove = oldBlockNamesSet - newBlockNamesSet
    blockNamesToAdd    = newBlockNamesSet - oldBlockNamesSet

    if blockNamesToRemove and blockNamesToAdd:
        print "[STAK] ERROR: Can't add & remove blocks at the same time, blockNamesToAdd", blockNamesToAdd, 'blockNamesToRemove', blockNamesToRemove
        sys.exit()

    removeFile = os.remove

    for name in blockNamesToRemove:
        fileName = oldBlockFiles[oldBlockNames.index(name)]
        removeFile(joinPath(packagePath, fileName + pyExt))

    for name in blockNamesToAdd:
        fileName = newBlockFiles[newBlockNames.index(name)]
        write(
            joinPath(packagePath, fileName + pyExt),
            ('from .block00_typing import *\n',)
        )
    # -----------------------------------------------------------------------------------------------------------------

    ## Make new by old blocks. For renaming in files & therefore excludes new blocks.
    # -----------------------------------------------------------------------------------------------------------------
    blockPrefix = cs.blockPrefix
    newByOldBlocks = []; append = newByOldBlocks.append
    enumOldBlockNames = list(enumerate(oldBlockNames))

    for newIdx, newName in enumerate(newBlockNames):
        for oldIdx, oldName in enumOldBlockNames:
            if oldName == newName:
                break
        else:
            continue

        oldIdxStr = str(oldIdx).zfill(oldMaxBlockIdxLen)
        newIdxStr = str(newIdx).zfill(newMaxBlockIdxLen)

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
        newBlockPath = joinPath(packagePath, newBlock + pyExt)
        append(newBlockPath)
        if oldBlock != newBlock:
            oldBlockPath = joinPath(packagePath, oldBlock + pyExt)
            renamePath(oldBlockPath, newBlockPath)
    # -----------------------------------------------------------------------------------------------------------------

    print 'blockPaths'
    for path in blockPaths:
        print path
    sys.exit()

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
