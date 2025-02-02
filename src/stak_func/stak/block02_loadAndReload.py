from functools import partial
from itertools import izip
from sys import modules

from . import __name__ as packageDotPath
from .block00_typing import *
from .z_utils import readBlockNames


def gimp(moduleDotPath, name):  # type: (str, str) -> Any
    """ Global import by name """
    return getattr(__import__(moduleDotPath), name)

itertools = partial(gimp, 'itertools')
functools = partial(gimp, 'functools')
sys       = partial(gimp, 'sys')

blockNames     = tuple(readBlockNames())
dotPathPrefix  = packageDotPath + '.'
blockDotPaths  = tuple((dotPathPrefix + name.rstrip('.py') for name in blockNames))
dotPathsByName = {name: path for name, path in izip(blockNames, blockDotPaths)}

def getBlocksByName(
        dotPaths    = blockDotPaths,  # type: Tup[str, ...]
        allModules  = modules,        # type: Dic[str, ModuleType]
        _blockNames = blockNames,     # type: Tup[str, ...]
        _izip       = izip            # type: Zip
):                                    # type: (...) -> Itrt[Tup[str, ModuleType]]
    return (
        (name, allModules[dotPath])
        for name, dotPath in _izip(_blockNames, dotPaths)
    )

def loadBlocks(dotPaths=blockDotPaths):  # type: (Tup[str, ...]) -> Itrt[ModuleType]
    for dotPath in dotPaths:
        yield __import__(dotPath)

blocks = tuple(loadBlocks())
blocksByName = {name: block for name, block in izip(blockNames, blocks)}

def reloadBlocks(_blocks=blocks):  # type: (Tup[ModuleType, ...]) -> None
    for block in _blocks:
        reload(block)

def bimp(blockName, _blocksByName=blocksByName):
    # type: (str, Dic[str, ModuleType]) -> ModuleType
    """ Import block by name """
    return _blocksByName[blockName]

def nimp(blockName, name, _blocksByName=blocksByName):
    # type: (str, str, Dic[str, ModuleType]) -> ModuleType
    """ Import name from block """
    return getattr(_blocksByName[blockName], name)


def run():
    pass
