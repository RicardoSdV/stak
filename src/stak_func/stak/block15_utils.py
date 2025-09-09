"""
Funcs used both outside & inside the package, avoid side effects & references to globals.
"""
import cPickle as pickle
from collections import deque, defaultdict
from functools   import partial, wraps
from itertools   import izip
from math        import floor, log10
from traceback   import print_stack, format_exc
from types       import FunctionType

from .block00_typing import *
from .               import block03_constants as cs

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

callTimes = []; appCallTimes = callTimes.append

def timeCalls(
        func,
        silenceTimers = cs.silenceTimers,
):
    if silenceTimers:
        return func

    name = func.__name__
    module = func.__module__
    key = (name, module)

    @wraps(func)
    def wrapper(*args, **kwargs):
        time = clock()
        res = func(*args, **kwargs)
        duration = clock() - time
        appCallTimes((key, duration))
        return res

    return wrapper


def getItem(accessor, accessible):
    return accessible[accessor]

getItem4 = partial(getItem, 4)


def roundToSigFigs(x, sigFigs):
    if x == 0:
        return 0
    return round(x, sigFigs - int(floor(log10(abs(x)))) - 1)


def printTimings():
    print '[STAK] printing timings'

    timesSum = defaultdict(float)
    callsSum = defaultdict(int)
    for key, duration in callTimes:
        timesSum[key] += duration
        callsSum[key] += 1

    means = []; app = means.append

    for key, timeSum in timesSum.iteritems():
        funcName, module = key
        reps = callsSum[key]
        mean = timeSum/reps
        mean = roundToSigFigs(mean, 3)
        timeSum = roundToSigFigs(timeSum, 3)
        app((module, funcName, timeSum, reps, mean))

    means.sort(key=getItem4, reverse=True)

    for module, funcName, timeSum, reps, mean in means:
        print '[STAK] calls: {:>6} | sum: {:>12.8f}s | mean: {:>12.8f}s | {:<25} | {:<25}'.format(
            reps, timeSum, mean, funcName, module)


def timeAllCallables(modules):  # type: (Itrb[ModuleType]) -> None
    if cs.silenceTimers:
        return

    for module in modules:
        moduleDict = module.__dict__
        for name, func in moduleDict.iteritems():
            if not isinstance(func, FunctionType):
                continue

            func = timeCalls(func)
            moduleDict[name] = func


class Cnt(object):
    __slots__ = ('cnt', )
    def __init__(self):
        self.cnt = 0
