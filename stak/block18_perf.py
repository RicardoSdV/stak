from .block00_autoImports import *

def timeCall(func):
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

def timeCalls(func):
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

def timeAllCallables():
    if not silenceTimers:
        for k, v in gSpace.iteritems():
            if isinstance(v, Function):
                gSpace[k] = timeCalls(v)

def printTimings():
    print '[STAK] printing timings'

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

    means.sort(key=getItem4, reverse=True)

    for module, funcName, timeSum, reps, mean in means:
        print '[STAK] calls: {:>6} | sum: {:>12.8f}s | mean: {:>12.8f}s | {:<25} | {:<25}'.format(
            reps, timeSum, mean, funcName, module)
