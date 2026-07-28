from .const import silenceTimers
from .lib import timeClock, sysModules, iterItems, Function, DefaultDict, funcToolsWraps
from .state import callTimesApp, callTimes
from .utils.log import INFO
from .utils.math import roundToSigFigs
from .utils.paths import packageDotPath

def timeCall(func):
    if silenceTimers:
        return func

    funcModule = func.__module__
    funcName = func.__name__

    @funcToolsWraps(func)
    def wrapper(*args, **kwargs):
        time = timeClock()
        res = func(*args, **kwargs)
        INFO('timeCall', funcModule, funcName, timeClock() - time, 's')
        return res
    return wrapper


def timeCalls(func):
    if silenceTimers:
        return func

    name = func.__name__
    module = func.__module__
    key = (name, module)

    @funcToolsWraps(func)
    def wrapper(*args, **kwargs):
        time = timeClock()
        res = func(*args, **kwargs)
        duration = timeClock() - time
        callTimesApp((key, duration))
        return res

    return wrapper


def timeAllCallables(dotPath=packageDotPath):
    if silenceTimers:
        return
    lenDotPath = len(dotPath)

    for k in sysModules:
        if k[:lenDotPath] != dotPath:
            continue

        moduleDict = sysModules[k].__dict__
        for k, v in iterItems(moduleDict):
            if not isinstance(v, Function):
                continue

            moduleDict[k] = timeCalls(v)


def printTimings():
    INFO('printing timings')

    timesSum = DefaultDict(float)
    callsSum = DefaultDict(int)
    for key, duration in callTimes:
        timesSum[key] += duration
        callsSum[key] += 1

    means = []; meansApp = means.append

    for key, timeSum in timesSum.iteritems():
        funcName, module = key
        reps = callsSum[key]
        mean = timeSum/reps
        mean = roundToSigFigs(mean, 3)
        timeSum = roundToSigFigs(timeSum, 3)
        meansApp((module, funcName, timeSum, reps, mean))

    means.sort(key=_getItem4, reverse=True)

    for module, funcName, timeSum, reps, mean in means:
        INFO('calls: {:>6} | sum: {:>12.8f}s | mean: {:>12.8f}s | {:<25} | {:<25}'.format(
            reps, timeSum, mean, funcName, module))

def _getItem4(acc):
    return acc[4]
