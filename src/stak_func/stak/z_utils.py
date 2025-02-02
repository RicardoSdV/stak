"""
Funcs used both outside & inside the package, avoid side effects & references to globals.
"""

from os import listdir
from re import compile as compileRegex

from .block00_typing import *
from .block01_settings import blockPrefix

matchNumAndSuffix = compileRegex(
    r'%s(\d+)_(.*)' % blockPrefix
).match

def getBlockNum(name):  # type: (str) -> int
    return int(matchNumAndSuffix(name).group(1))

def readBlockNames(path='.', listDir=listdir, prefix=blockPrefix):
    # type: (str, Cal[[str], Lst[str]], str) -> Itrt[str]
    return (n for n in listDir(path) if n.startswith(prefix))

def readSortedBlockNames(path='.'):
    return sorted(readBlockNames(path), key=getBlockNum)

def read(path):  # type: (str) -> Lst[str]
    with open(path, 'r') as f:
        return f.readlines()

def padFlags(flags):  # type: (Seq[str]) -> Itrt[str]
    maxFlagLen = max(len(flag) for flag in flags)
    return (': ' + flag + (' '*(maxFlagLen - len(flag))) + ': '
            for flag in flags)
