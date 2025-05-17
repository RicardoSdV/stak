"""
Funcs used both outside & inside the package, avoid side effects & references to globals.
"""
import gzip
import json
from functools import partial
from importlib import import_module
from itertools import izip
from os import listdir
from os.path import abspath, dirname
from re import compile as compileRegex
from traceback import print_stack

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

def readJson(path):  # type: (str) -> Any
    with open(path, 'r') as f:
        return json.load(f)

def writeJson(path, data):  # type: (str, Any) -> None
    with open(path, 'w') as f:
        json.dumps(data)

def writeGzip(path, data):  # type: (str, Any) -> None
    with gzip.open(path, 'w') as f:
        json.dumps(data, f)

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

red = 31
grey = 90

def colorStr(code, _str):
    return '\033[{code}m{_str}\033[0m'.format(code=code, _str=_str)

def tryCall(_callable, *args, **kwargs):  # type: (Cal, *Any, **Any) -> Any
    errMess = kwargs.pop('errMess', None)
    try:
        return _callable(*args, **kwargs)
    except Exception as e:
        if errMess: E(errMess, exception=e)
        else      : E(exception=e)

def serializeArgs(frame, args, kwargs, exclFromLocals={'self', 'cls'}, izip=izip):
    # type: (Opt[FrameType], Tup[Any, ...], Dic[str, Any], Set[str], Zip) -> Itrt[Tup[str, str]]

    args = iter(args)
    while args:
        k = next(args, 'noKeyFound')
        v = next(args, 'noValFound')

        if k == 'noKeyFound' and v == 'noValFound':
            break

        if k != 'noKeyFound' and v != 'noValFound':
            yield str(k), str(v)
            continue

        yield 'noKeyFound', str(k)

    for k, v in kwargs.iteritems():
        yield k, str(v)

    if frame:
        for k, v in frame.f_locals.iteritems():
            if k not in exclFromLocals and k not in kwargs:
                yield k, str(v)

def argsToStr(serializedArgs):  # type: (Itrb[Tup[str, str]]) -> str
    return ', '.join(
        k + '=' + v
        if k != 'noKeyFound'
        else v
        for k, v in serializedArgs
    )

def LOG(tag, color, printStack, message='', *args, **kwargs):
    serializedArgs = serializeArgs(None, args, kwargs)
    strArgs = argsToStr(serializedArgs)
    mess = ' '.join(('[STAK]', str(tag), str(message), str(strArgs)))
    if printStack: print_stack()
    print colorStr(color, mess)

P = partial(LOG, '[PRINT]', grey, False)
E = partial(LOG, '[ERROR]', red, True)
