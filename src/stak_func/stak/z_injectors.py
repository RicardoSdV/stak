"""
Some stuff is more convenient if computed, but really it only needs to be computed once, not every time the program is run.
So, the solution is to compute these things in this file & inject the results into stak.
Also, removes some clutter from the code.
Also, settings are injected by running this.

Since blocks are numbered it is very tedious to insert or delete a new block, yes it is essential that they be numbered.
running this file will rename the appropriate files when one of them is deleted & insert & rename when "newBlockName" is
provided & more. If this file could rename itself, then it cannot be numbered itself.
"""

import sys
import os

from collections import defaultdict
from itertools   import chain, izip

from .block00_typing         import *
from . import block01_settings   as settings
from . import block02_settingObj as settingObj
from . import block03_constants  as cs
from .block15_utils          import read, write


osPath   = os.path
abspath  = osPath.abspath
joinPath = osPath.join
dirname  = osPath.dirname

pyExt          =  cs.pyExt
nLenPyExt      = -cs.lenPyExt
pycExt         =  cs.pycExt
nLenPycExt     = -cs.lenPycExt
blockPrefix    =  cs.blockPrefix
lenBlockPrefix =  cs.lenBlockPrefix

def replaceInPlace(lines, lookingFor, dataStructure):  # type: (Lst[str], str, Any) -> None
    for i, line in enumerate(lines):
        if line.startswith(lookingFor):
            lines[i] = '%s%r\n  # Injected by block15_injectors.py' % (lookingFor, dataStructure)
            return
    print '[STAK] ERROR: Looking for', lookingFor, 'prefix & not found'


# Read lazy, written on exit.
linesByPath = {}  # type: Dic[str, Lst[str]]

def getLinesForPath(_path, _linesByPath=linesByPath):  # type: (str, ...) -> Lst[str]
    if _path not in _linesByPath:
        _linesByPath[_path] = read(_path)
    return _linesByPath[_path]

linesByName = {}
pathsByName = {}
def getLinesForName(name):
    if name not in linesByName:
        path = pathsByName[name]
        linesByName[name] = read(path)
    return linesByName[name]


# Parse dir files
packagePath = dirname(abspath(__file__))
oldStakFiles = os.listdir(packagePath)
oldPyFileNames = [name[:nLenPyExt] for name in oldStakFiles if name[nLenPyExt:] == pyExt]
oldBlockFileNames = [name for name in oldPyFileNames if name[:lenBlockPrefix] == blockPrefix]

# Make old block files names and indexes
# ---------------------------------------------------------------------------------------------------------------------
oldBlockFiles   = []; oldBlockFilesApp   = oldBlockFiles.append
nonBlockFiles   = []; nonBlockFilesApp   = nonBlockFiles.append
oldBlockNames   = []; oldBlockNamesApp   = oldBlockNames.append
oldBlockStrIdxs = []; oldBlockStrIdxsApp = oldBlockStrIdxs.append

for file in os.listdir(packagePath):
    if file[nLenPyExt:] != pyExt:
        continue
    file = file[:nLenPyExt]

    if file[:lenBlockPrefix] != blockPrefix:
        nonBlockFilesApp(file)
        pathsByName[file] = joinPath(packagePath, file + pyExt)
        continue

    oldBlockFilesApp(file)
    file = file[lenBlockPrefix:]
    idx, name = file.split('_')
    oldBlockStrIdxsApp(idx)
    oldBlockNamesApp(name)
# ---------------------------------------------------------------------------------------------------------------------

## Make newBlockFiles
# ---------------------------------------------------------------------------------------------------------------------
newBlockNames = cs.blockNames
oldMaxBlockIdxLen = len(str(len(oldBlockNames) - 1))
newMaxBlockIdxLen = len(str(len(newBlockNames) - 1))
newBlockFiles = [
    blockPrefix + str(i).zfill(newMaxBlockIdxLen) + '_' + name
    for i, name in enumerate(newBlockNames)
]
# ---------------------------------------------------------------------------------------------------------------------


## On blocks changed run block injection
# ---------------------------------------------------------------------------------------------------------------------
if oldBlockFiles == newBlockFiles:
    for file, name in izip(oldBlockFiles, oldBlockNames):
        pathsByName[name] = joinPath(packagePath, name + pyExt)
else:
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

        if not input('DANGER sure of removing: %s ??' % fileName):
            sys.exit()

        removeFile(joinPath(packagePath, fileName + pyExt))

    for name in blockNamesToAdd:
        fileName = newBlockFiles[newBlockNames.index(name)]
        path = joinPath(packagePath, fileName + pyExt)
        pathsByName[name] = path
        write(path, ('from .block00_typing import *\n',))
    # -----------------------------------------------------------------------------------------------------------------

    ## Make new by old blocks. For renaming in files & therefore excludes new blocks.
    # -----------------------------------------------------------------------------------------------------------------
    blockPrefix = cs.blockPrefix
    newByOldBlocks = []
    newByOldBlocksApp = newByOldBlocks.append
    enumOldBlockNames = list(enumerate(oldBlockNames))

    for newIdx, newName in enumerate(newBlockNames):
        for oldIdx, oldName in enumOldBlockNames:
            if oldName == newName:
                break
        else:
            continue

        newByOldBlocksApp(
            (
                oldBlockFiles[oldIdx],
                blockPrefix + str(newIdx).zfill(newMaxBlockIdxLen) + '_' + newName,
            )
        )
    # -----------------------------------------------------------------------------------------------------------------

    ## Rename block files.
    # -----------------------------------------------------------------------------------------------------------------
    renamePath = os.rename
    for oldBlock, newBlock in newByOldBlocks:
        name = newBlockNames[newBlockFiles.index(newBlock)]
        newBlockPath = joinPath(packagePath, newBlock + pyExt)
        pathsByName[name] = newBlockPath

        if oldBlock != newBlock:
            oldBlockPath = joinPath(packagePath, oldBlock + pyExt)
            renamePath(oldBlockPath, newBlockPath)
    # -----------------------------------------------------------------------------------------------------------------

    ## Rename references to blocks, sortBlock imports.
    # -----------------------------------------------------------------------------------------------------------------
    for name in chain(newBlockNames, nonBlockFiles):
        lines = getLinesForName(name)

        importsStarted = importsFinished = False
        import_blockAndLine = []; import_blockAndLineApp = import_blockAndLine.append
        lineNos = []; lineNosApp = lineNos.append

        for i, line in enumerate(lines):

            # Rename references to blocks
            for oldBlock, newBlock in newByOldBlocks:
                if oldBlock in line:
                    line = line.replace(oldBlock, newBlock)
                    lines[i] = line

            # Sort imports, only block imports which should be all together by codestyle.
            if importsFinished:
                continue

            if 'import ' in line:
                for block in newBlockFiles:
                    if block in line:
                        importsStarted = True
                        import_blockAndLineApp((block, line))
                        lineNosApp(i)
                        break

            elif importsStarted:
                importsFinished = True

        if importsStarted and importsFinished:

            import_blockAndLine.sort()

            for (block, line), lineNo in izip(import_blockAndLine, lineNos):
                lines[lineNo] = line

        elif not importsStarted and not importsFinished:
            continue
        else:
            print '[STAK] ERROR: Imports sorting. started', importsStarted, 'finished', importsFinished
# ---------------------------------------------------------------------------------------------------------------------

## Run manual injectors.
# ---------------------------------------------------------------------------------------------------------------------
if cs.runInjectors:
    def blockNameFromModule(module):  # type: (ModuleType) -> str
        return module.__name__.split('_')[-1]

    # Settings injection
    # -----------------------------------------------------------------------------------------------------------------
    settingsLines   = getLinesForName(blockNameFromModule(settings))
    settingObjLines = getLinesForPath(blockNameFromModule(settingObj))

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
    padByNotAllFlags = {flag: pFlag for flag, pFlag in izip(allFlags, pAllFlags)}

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
    constsLines = getLinesForPath(blockNameFromModule(cs))

    replaceInPlace(constsLines, 'paddedStdFlags = '     , paddedStdFlags)
    replaceInPlace(constsLines, 'pStakFlags = '         , paddedStakFlags)
    replaceInPlace(constsLines, 'pTraceFlags = '        , paddedTraceFlags)
    replaceInPlace(constsLines, 'pStdFlagsByStdFlags = ', padByNotStdFlags)
    replaceInPlace(constsLines, 'allPflagsByFlags = '   , padByNotAllFlags)
    replaceInPlace(constsLines, 'wholeEnoughs = '       , wholeEnoughFlags)
    replaceInPlace(constsLines, 'runInjectors = '       , 0)
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


## Write all lines.
# ---------------------------------------------------------------------------------------------------------------------
for name, lines in linesByName.iteritems():
    path = pathsByName[name]
    write(path, lines)
# ---------------------------------------------------------------------------------------------------------------------


## Unload all blocks
# ---------------------------------------------------------------------------------------------------------------------
modules = sys.modules
packageDotPathPrefix = '.'.join(__name__.split('.')[:-1]) + '.'
for name in newBlockNames:
    moduleDotPath = packageDotPathPrefix + name
    if moduleDotPath in modules:
        module = modules.pop(moduleDotPath)
        del module
# ---------------------------------------------------------------------------------------------------------------------
