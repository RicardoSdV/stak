"""
Funcs used both outside & inside the package, avoid side effects & references to globals.
"""
from functools import partial
import traceback
from importlib import import_module
from os import listdir
from os.path import abspath, dirname
from re import compile as compileRegex

from . import __name__ as packageDotPath
from .block00_typing import *
from .block03_constants import blockPrefix

matchNumAndSuffix = compileRegex(
    blockPrefix + r'(\d+)_(.*)'
).match

packageName = __name__.split('.')[-2]
packagePath = dirname(abspath(__file__))

def getBlockNum(name):  # type: (str) -> int
    return int(matchNumAndSuffix(name).group(1))

def readBlockNames(path=packagePath):  # type: (str) -> Itrt[str]
    for name in listdir(path):
        if name.startswith(blockPrefix) and not name.endswith('.pyc'):
            yield name

def readSortedBlockNames(path=packagePath):  # type: (str) -> Lst[str]
    return sorted(readBlockNames(path), key=getBlockNum)

def read(path):  # type: (str) -> Lst[str]
    with open(path, 'r') as f:
        return f.readlines()

def write(path, lines):  # type: (str, Itrb[str]) -> None
    with open(path, 'w') as f:
        f.writelines(lines)

def padFlags(flags):  # type: (Seq[str]) -> Itrt[str]
    maxFlagLen = max(len(flag) for flag in flags)
    for flag in flags:
        yield ': ' + flag + (' ' * (maxFlagLen - len(flag))) + ': '

def getBlockDotPaths():  # type: () -> Itrt[str]
    prefix = packageDotPath + '.'
    for name in readBlockNames():
        yield prefix + name.rstrip('.py')

def loadBlocks():  # type: () -> Itrt[ModuleType]
    for dotPath in getBlockDotPaths():
        module = tryCall(import_module, dotPath)
        if module:
            yield reload(module)

def colorStr(code, _str):
    return '\033[{code}m{_str}\033[0m'.format(code=code, _str=_str)

redStr = partial(colorStr, 31)

def tryCall(_callable, *args, **kwargs):  # type: (Cal, *Any, **Any) -> Any
    errMess = kwargs.pop('errMess', None)
    try:
        return _callable(*args, **kwargs)
    except:
        if errMess: print redStr('ERROR: ' + errMess)
        traceback.print_stack()

object
