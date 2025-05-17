"""
Since blocks are numbered it is very tedious to insert or delete a new block,
running this file will rename the appropriate files when one of them is deleted
& insert & rename when "newBlockName" is provided automatically.
"""

from functools import partial
from itertools import izip
from os import rename
from os.path import join

from src.stak_func.stak.block00_typing import *
from src.stak_func.stak.z_utils import getBlockNum, matchNumAndSuffix, readSortedBlockNames, read, write

## Settings
# In the format: {prefix or ''}{index}_{name}{suffix or ''}
newBlockName = ''
blockPrefix = 'block'
fileExtension = '.py'
dirPath = 'stak'

## For internal use, (not settings)
maxLen = 2

if newBlockName:
    if not newBlockName.endswith(fileExtension): newBlockName += fileExtension
    if not newBlockName.startswith(blockPrefix): newBlockName = blockPrefix + newBlockName


def runAll():  # type: () -> None
    blockInjectors = runAllBlockNameManip()

    blockNames = readSortedBlockNames(dirPath)
    blockNames.append('__init__.py')

    linesInjectors = blockInjectors
    lineInjectors = {}
    fileInjectors = [partial(sortBlockNameImportsInPlace, blockNames)]

    linesByBlock = readBlocks(blockNames)
    print 'linesByBlock', linesByBlock

    if not linesInjectors and not lineInjectors:
        return

    applyInjectorsMaybeToLinesInPlace(linesByBlock, linesInjectors, lineInjectors, fileInjectors)

    writeBlocks(linesByBlock)

""" ========================================= CREATE & RENAME BLOCKS ============================================== """

def runAllBlockNameManip():  # type: () -> Lst[Cal[[str], str]]
    """
    If any block in dirPath was deleted, all the blocks with higher indices will be decreased.

    If appropriate newBlockName is provided, a new file with this name will be created, & all
    the other blocks with indices >= newBlockName index will be incremented.

    If any blocks were renamed all blocks will be searched for references to the old block names
    & replaced with the new block names.

    All block names are zero padded.

    No lines are actually modified, a list of injectors is returned to be applied later on.
    """
    injectors = []

    # Gap filling
    oldBlockNames = readSortedBlockNames(dirPath)

    gaplessBlockNames = fillGaps(oldBlockNames)
    zeroPadGaplessNames = zeroPadNames(gaplessBlockNames)
    renameBlocks(oldBlockNames, zeroPadGaplessNames)

    if oldBlockNames != zeroPadGaplessNames:
        newByOldNames = makeNewByOldNames(oldBlockNames, zeroPadGaplessNames)

        injectors.append(
            partial(replaceOldBlockNamesWithNew, newByOldNames)
        )

    # New block creation
    global newBlockName, maxLen

    namesForMaxLen = zeroPadGaplessNames + [newBlockName] if newBlockName else zeroPadGaplessNames
    maxLen = longestNumLen(strNumsFromBlockNames(namesForMaxLen))

    if newBlockName:
        newBlockName = zeroPadName(newBlockName)

    if newBlockName and newBlockName not in gaplessBlockNames:
        createNewBlock(newBlockName)

        newByOldNames = makeNewByOldNames(
            gaplessBlockNames,
            incrementGreaterThanNewBlockNums(gaplessBlockNames)
        )

        paddedNewByOld = {}
        for old, new in newByOldNames.iteritems():
            paddedNewByOld[zeroPadName(old)] = zeroPadName(new)

        injectors.append(
            partial(replaceOldBlockNamesWithNew, paddedNewByOld)
        )

    return injectors

def zeroPadName(name):
    return joinBlockName(
        num=getBlockStrNum(name).lstrip('0').zfill(maxLen),
        suffix=getBlockSuffix(name)
    )

def fillGaps(names):  # type: (Lst[str]) -> Lst[str]
    return [
        joinBlockName(i, getBlockSuffix(name))
        for i, name in enumerate(names)
    ]

def strNumsFromBlockNames(names):  # type: (Itrb[str]) -> Lst[str]
    return [getBlockStrNum(name).lstrip('0') for name in names]

def longestNumLen(strNums):  # type: (Itrb[str]) -> int
    return max((len(num) for num in strNums))

def zeroPadNames(names):  # type: (Itrb[str]) -> Lst[str]
    strNums = strNumsFromBlockNames(names)
    maxNum = longestNumLen(strNums)
    paddedNums = (num.zfill(maxNum) for num in strNums)
    suffixes = (getBlockSuffix(name) for name in names)
    return [joinBlockName(num, suffix) for num, suffix in izip(paddedNums, suffixes)]

def incrementGreaterThanNewBlockNums(oldBlockNames):  # type: (Lst[str]) -> Itrt[str]
    """ Iter old block names, yield old names unless newBlockIndex found, in that case yield
    the new block name & the rest of the old block names but incremented by one. """
    newBlockIndex = getBlockNum(newBlockName)
    newNameIndexFound = False
    for i, name in enumerate(oldBlockNames):

        if i < newBlockIndex:
            yield name
        elif i == newBlockIndex:
            newNameIndexFound = True
            yield newBlockName

        if newNameIndexFound:  # i > newBlockNum:
            incName = incrementBlockName(name)
            zPadIncName = zeroPadName(incName)
            renameBlock(zeroPadName(name), zPadIncName)
            yield incName

    if not newNameIndexFound:  # Index >= len(names)
        yield newBlockName

""" =============================================================================================================== """

""" ================================================ INJECTING ==================================================== """

def replaceOldBlockNamesWithNew(newByOldBlockNames, line):  # type: (Dic[str, str], str) -> Opt[str]
    for oldName, newName in newByOldBlockNames.iteritems():
        line = line.replace(oldName, newName)
    return line

def applyInjectorsMaybeToLinesInPlace(linesByBlock, linesInjectors, lineInjectors, fileInjectors):
    # type: (Dic[str, Lst[str]], Lst[Cal[[str], str]], Dic[str, Cal[[str], str]], Lst[Cal[[Lst[str]]]]) -> None
    """
    Apply lines injectors to every line.
    Apply line injectors to their appropriate line. (Not in use, planned for merge with injectors.py)
    Apply file injectors to all the lines of every file. (To sort imports)
    """

    for blockName, lines in linesByBlock.iteritems():
        for i, line in enumerate(lines):
            for linesInjector in linesInjectors:
                lines[i] = linesInjector(line)

            for lookingFor, lineInjector in lineInjectors.iteritems():
                if line.startswith(lookingFor):
                    lines[i] = lineInjector(line)
                    del lineInjectors[lookingFor]
                    break

        for injector in fileInjectors:
            injector(lines)

def sortBlockNameImportsInPlace(blockNames, lines):  # type: (Lst[str], Lst[str]) -> None
    imports, lineNums = [], []
    for i, line in enumerate(lines):
        if any((name in line for name in blockNames)):
            imports.append(line)
            lineNums.append(i)

    imports.sort()
    for num, _import in izip(lineNums, imports):
        lines[num] = _import

""" =============================================================================================================== """

""" ================================================ BLOCK OPS ==================================================== """

def renameBlock(oldName, newName):  # type: (str, str) -> None
    rename(join(dirPath, oldName), join(dirPath, newName))

def renameBlocks(oldNames, newNames):  # type: (Itrb[str], Itrb[str]) -> None
    for oldName, newName in izip(oldNames, newNames):
        renameBlock(oldName, newName)

def readBlock(name):  # type: (str) -> Lst[str]
    blockPath = join(dirPath, name)
    blockLines = read(blockPath)
    return blockLines

def readBlocks(names):  # type: (Itrb[str]) -> Dic[str, Lst[str]]
    return {
        name: readBlock(name)
        for name in names
    }

def writeBlocks(linesByBlock):  # type: (Dic[str, Lst[str]]) -> None
    for blockName, lines in linesByBlock.iteritems():
        write(join(dirPath, blockName), lines)

def createNewBlock(name):  # type: (str) -> None
    write(join(dirPath, name), ['from .block00_typing import *'])

""" =============================================================================================================== """

""" ================================================ NAME OPS ===================================================== """


def getBlockStrNum(name):  # type: (str) -> str
    return matchNumAndSuffix(name).group(1)

def getBlockSuffix(name):  # type: (str) -> str
    return matchNumAndSuffix(name).group(2)

def getBlockNumAndSuffix(name):  # type: (str) -> Tup[int, str]
    match = matchNumAndSuffix(name)
    return int(match.group(1)), match.group(2)

def joinBlockName(num, suffix):  # type: (Uni[int, str], str) -> str
    return 'block{}_{}'.format(num, suffix)

def incrementBlockName(name):  # type: (str) -> str
    num, suffix = getBlockNumAndSuffix(name)
    num += 1
    return joinBlockName(num, suffix)

def makeNewByOldNames(oldNames, newNames):  # type: (Lst[str], Itrb[str]) -> Dic[str, str]
    newByOgBlockNames = {}
    zippedOgs = zip(oldNames, (getBlockSuffix(name) for name in oldNames))
    for newName in newNames:
        newSuffix = getBlockSuffix(newName)
        for oldName, oldSuffix in zippedOgs:
            if oldSuffix == newSuffix:
                newByOgBlockNames[oldName.rstrip('.py')] = newName.rstrip('.py')
                break
    assert len(newByOgBlockNames) == len(oldNames), 'Could be that two blocks have the same suffix, they must be unique.'
    return newByOgBlockNames

""" =============================================================================================================== """


if __name__ == '__main__':
    runAll()
