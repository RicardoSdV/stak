"""
Funcs used both outside & inside the package, avoid side effects & references to globals.
"""
import cPickle as pickle
from collections import deque
from functools   import partial, wraps
from importlib   import import_module
from itertools   import izip
from os          import listdir
from os.path     import abspath, dirname
from re          import compile as compileRegex
from traceback   import print_stack, format_exc

from .block00_typing    import *
from .                  import __name__ as packageDotPath, block03_constants as cs


matchNumAndSuffix = compileRegex(
    cs.blockPrefix + r'(\d+)_(.*)'
).match

packageName = __name__.split('.')[-2]
packagePath = dirname(abspath(__file__))

def getBlockNum(name):  # type: (str) -> int
    return int(matchNumAndSuffix(name).group(1))

def readBlockNames(path=packagePath):  # type: (str) -> Lst[str]
    blockNames = [
        name
        for name in listdir(path)
        if name.startswith(cs.blockPrefix) and not name.endswith('.pyc')
    ]
    blockNames.sort(key=getBlockNum)
    return blockNames

def loadBlocks(prefix = packageDotPath + '.'):  # type: (str) -> Lst[ModuleType]
    blocks = []; append = blocks.append

    for blockName in readBlockNames():
        blockDotPath = prefix + blockName[:-3]
        module = tryCall(import_module, blockDotPath)
        if module:
            append(module)

    return blocks

def read(path):  # type: (str) -> Lst[str]
    with open(path, 'r') as f:
        return f.readlines()

def write(path, lines):  # type: (str, Itrb[str]) -> None
    with open(path, 'w') as f:
        f.writelines(lines)

def writePickle(path, data):
    with open(path, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

def readPickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

red = 31
grey = 90

def colorStr(code, _str):
    return '\033[{code}m{_str}\033[0m'.format(code=code, _str=_str)

def tryCall(_callable, *args, **kwargs):  # type: (Cal, *Any, **Any) -> Any
    errMess = kwargs.pop('errMess', None)
    try:
        return _callable(*args, **kwargs)
    except Exception as e:
        if errMess: E(errMess, exception=format_exc())
        else      : E(exception=format_exc())


class NoKeyFound(object): pass
class NoValFound(object): pass


def serializeArgs(frame, args, kwargs, exclFromLocals=cs.exclFromLocals, izip=izip):
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

    # TODO: Theres a bug here where self gets to kwargs for some reason.
    for k, v in kwargs.iteritems():
        yield k, str(v)

    if not frame:
        return

    for k, v in frame.f_locals.iteritems():
        if k in exclFromLocals:
            continue

        if k in kwargs:
            continue

        yield k, str(v)


def argsToStr(serializedArgs, commaJoin=', '.join):  # type: (Itrb[Tup[str, str]], Join) -> str
    return commaJoin(
        k + '=' + v
        if k is not NoKeyFound
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
E = partial(LOG, '[ERROR]', red , True )


def funcErr(*_, **__):
    print ('ERROR: This noop function is here purely to avoid '
           'squiggly lines in PyCharm, which make me very nervous, '
           'but the code is supposed to fail if this is not '
           'overridden, printing callstack now.')
    print_stack()
    return

def makeObjErr(_class):
    class ObjectError(_class): pass
    for k, v in _class.__dict__.iteritems():
        if k[:2] != '__' and callable(v):
            tryCall(setattr, ObjectError, k, funcErr)
    return ObjectError()

listErr = makeObjErr(list)
dequeErr = makeObjErr(deque)


def log(*args):
    # ToDo: There should be a better internal logging, LOG()
    #  does not work too well, printing colours is not env
    #  friendly, just use a wrapper over print for now.
    print '[STAK]', ' '.join((str(arg) for arg in args))


def timeCall(func, silenceTimers=cs.silenceTimers):
    if silenceTimers:
        return func

    funcModule = func.__module__
    funcName = func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        time = clock()
        res = func(*args, **kwargs)
        log('timeCall', funcModule, funcName, clock() - time, 's')
        return res
    return wrapper

callTimes = {}
callReps = {}

def timeCalls(
        func,
        silenceTimers = cs.silenceTimers,
        callTimes = callTimes,
        callReps = callReps,
):
    if silenceTimers:
        return func

    name = func.__name__
    module = func.__module__
    key = (name, module)
    callTimes[key] = 0.0
    callReps[key] = 0.0

    @wraps(func)
    def wrapper(*args, **kwargs):
        time = clock()
        res = func(*args, **kwargs)
        duration = clock() - time
        callTimes[key] += duration
        callReps[key] += 1
        return res

    return wrapper


def getItem(accessor, accessible):
    return accessible[accessor]

returnIdx4 = partial(getItem, 4)


def printTimings():
    print '[STAK] printing timings'

    res = []; app = res.append

    for key, timeSum in callTimes.iteritems():
        reps = callReps[key]
        funcName, module = key
        mean = timeSum/reps
        app((funcName, module, timeSum, reps, mean))

    res.sort(key=returnIdx4, reverse=True)

    for el in res:
        print el





class Cnt(object):
    __slots__ = ('cnt', )
    def __init__(self):
        self.cnt = 0
