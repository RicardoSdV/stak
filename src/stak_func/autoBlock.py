"""
Since blocks are numbered it is very tedious to insert or delete a new block,
running this file will rename the appropriate files when one of them is deleted
& insert & rename when "newBlockName" is provided automatically.
"""
#### Interface
__all__ = ()

class SettingsFactory(object):
    """ When importing this file modify the object instantiated
    by this class to override the defaults """

    __slots__ = ('__newBlockName', 'dirPath', 'blockPrefix', 'fileExtension')

    def __init__(self):  # type: () -> None
        # In the format: {prefix or ''}{index}_{name}{suffix or ''}
        self.__newBlockName = ''

        # Dir where all blocks are to be found
        self.dirPath = 'stak'

        self.blockPrefix = 'block'
        self.fileExtension = '.py'

    @property
    def newBlockName(self):
        newBlockName = self.__newBlockName
        if newBlockName:
            if not newBlockName.endswith(self.fileExtension):
                newBlockName += self.fileExtension
            if not newBlockName.startswith(self.blockPrefix):
                newBlockName = self.blockPrefix + newBlockName
        return newBlockName


settings = SettingsFactory()


from functools import partial
from os import listdir, rename
from os.path import join
from re import compile
from typing import *


def runAll():  # type: () -> None
    blockInjectors = runAllBlockNameManip()

    linesInjectors = blockInjectors
    lineInjectors = {}

    if not (linesInjectors or lineInjectors):
        return

    blockNames = readAndSortBlockNames()
    linesByBlock = readBlocks(blockNames)

    applyInjectorsMaybeToLinesInPlace(linesByBlock, linesInjectors, lineInjectors)

    writeBlocks(linesByBlock)


""" ========================================= CREATE & RENAME BLOCKS ============================================== """

def runAllBlockNameManip():  # type: () -> List[Callable[[str], str]]
    """
    If any block in dirPath was deleted, all the blocks with higher indices will be decreased.

    If appropriate newBlockName is provided, a new file with this name will be created, & all
    the other block with indices >= newBlockName index will be incremented.

    If any block(s) was/were renamed all the blocks will be searched for references to the old
    block name(s) & replaced with the new block name(s), through the mechanism of returning a
    list of injector partials to be applied to the lines later on.
    """
    injectors = []
    newBlockName = settings.newBlockName

    # Gap filling
    ogBlockNames = readAndSortBlockNames()
    gaplessBlockNames = fillGapsAndRenameFiles(ogBlockNames)

    if ogBlockNames != gaplessBlockNames:
        injectors.append(
            partial(
                replaceOldBlockNamesWithNew,
                makeNewByOldNames(ogBlockNames, gaplessBlockNames),
            )
        )

    # New block creation
    if newBlockName and newBlockName not in gaplessBlockNames:
        createNewBlock(newBlockName)
        injectors.append(
            partial(
                replaceOldBlockNamesWithNew,
                makeNewByOldNames(
                    gaplessBlockNames,
                    incrementGreaterThanNewBlockNums(gaplessBlockNames)
                )
            )
        )

    return injectors

def fillGapsAndRenameFiles(ogNames):  # type: (List[str]) -> List[str]
    """ Ensure all indexes increment by one, e.g. if a block is deleted might result in an increment of 2 or more between
    blocks, this func will rename the files to remove this gap & returns a new list of the gapless names. """
    result = ogNames[:]
    for i, oldName in enumerate(result):
        newName = joinBlockName(i, getBlockSuffix(oldName))
        renameBlock(oldName, newName)
        result[i] = newName
    return result

def incrementGreaterThanNewBlockNums(oldBlockNames):  # type: (List[str]) -> Iterator[str]
    """ Iter old block names, yield old names unless newBlockIndex found, in that case yield
    the new block name & the rest of the old block names but incremented by one. """
    newBlockName = settings.newBlockName
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
            renameBlock(name, incName)
            yield incName

    if not newNameIndexFound:  # Index >= len(names)
        yield newBlockName

""" =============================================================================================================== """

""" ================================================ INJECTING ==================================================== """

def replaceOldBlockNamesWithNew(newByOldBlockNames, line):  # type: (Dict[str, str], str) -> Optional[str]
    for oldName, newName in newByOldBlockNames.iteritems():
        line = line.replace(oldName, newName)
    return line

def applyInjectorsMaybeToLinesInPlace(linesByBlock, linesInjectors, lineInjectors):
    # type: (Dict[str, List[str]], List[Callable[[str], str]], Dict[str, Callable[[str], str]]) -> None
    """ Apply lines injectors to every line, & line injectors to their appropriate line """
    for blockName, lines in linesByBlock.iteritems():
        for i, line in enumerate(lines):

            for linesInjector in linesInjectors:
                lines[i] = linesInjector(line)

            for lookingFor, lineInjector in lineInjectors.iteritems():
                if line.startswith(lookingFor):
                    lines[i] = lineInjector(line)
                    del lineInjectors[lookingFor]
                    break

""" =============================================================================================================== """

""" ================================================ BLOCK OPS ==================================================== """

def renameBlock(oldName, newName):  # type: (str, str) -> None
    rename(join(settings.dirPath, oldName), join(settings.dirPath, newName))

def readAndSortBlockNames():  # type: () -> List[str]
    return sorted(
        (
            name for name in listdir(settings.dirPath)
            if name.startswith('block') and name.endswith('.py')
        ),
        key=getBlockNum,
    )

def readBlock(name):  # type: (str) -> List[str]
    with open(join(settings.dirPath, name), 'r') as block:
        return block.readlines()

def readBlocks(names):  # type: (Iterable[str]) -> Dict[str: List[str]]
    return {
        name: readBlock(name)
        for name in names
    }

def writeBlocks(linesByBlock):  # type: (Dict[str, List[str]]) -> None
    for blockName, lines in linesByBlock.iteritems():
        with open(join(settings.dirPath, blockName), 'w') as blockFile:
            blockFile.writelines(lines)

def createNewBlock(name):
    with open(join(settings.dirPath, name), 'w') as _:
        pass

""" =============================================================================================================== """

""" ================================================ NAME OPS ===================================================== """

matchNumAndSuffix = compile(r'block(\d+)_(.*)').match

def getBlockNum(name):  # type: (str) -> int
    return int(matchNumAndSuffix(name).group(1))

def getBlockSuffix(name):  # type: (str) -> str
    return matchNumAndSuffix(name).group(2)

def getBlockNumAndSuffix(name):  # type: (str) -> Tuple[int, str]
    match = matchNumAndSuffix(name)
    return int(match.group(1)), match.group(2)

def joinBlockName(num, suffix):  # type: (int, str) -> str
    return 'block{}_{}'.format(num, suffix)

def incrementBlockName(name):  # type: (str) -> str
    num, suffix = getBlockNumAndSuffix(name)
    num += 1
    return joinBlockName(num, suffix)

def makeNewByOldNames(oldNames, newNames):  # type: (List[str], Iterable[str]) -> Dict[str, str]
    newByOgBlockNames = {}
    zippedOgs = zip(oldNames, (getBlockSuffix(name) for name in oldNames))
    for newName in newNames:
        newSuffix = getBlockSuffix(newName)
        for oldName, oldSuffix in zippedOgs:
            if oldSuffix == newSuffix:
                newByOgBlockNames[oldName.rstrip('.py')] = newName.rstrip('.py')
                break
    assert len(newByOgBlockNames) == len(oldNames)
    return newByOgBlockNames

""" =============================================================================================================== """


if __name__ == '__main__':
    runAll()
