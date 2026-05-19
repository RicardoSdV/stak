from .block00_autoImports import *

def tryCall(_callable, *args, **kwargs):  # type: (Cal, *Any, **Any) -> Any
    errMess = kwargs.pop('errMess', None)
    try:
        return _callable(*args, **kwargs)
    except Exception as e:
        if errMess: E(errMess, exception=formatExc())
        else      : E(exception=formatExc())

def serializeArgs(frame, args, kwargs):
    # type: (Opt[Frame], Tup[Any, ...], Dic[str, Any]) -> Itrt[Tup[str, str]]

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

def printStack(frameNum=1):
    frame = sysGetFrame(frameNum)
    for el in formatStack(frame):
        print(('[STAK] FRAME: %s' % el).rstrip('\n'))

def INFO(message, *args):
    print('[STAK] INFO : %s' % (message % args))
    return True

def DEBUG(message='', *args):
    if logPyInternal:
        print('[STAK] DEBUG: %s' % (message % args))
    return True

def ERROR(message='', *args):
    print('[STAK] ERROR: %s' % (message % args))
    printStack(2)
    return True

def EXCEPTION(message='', exc=None, *args):
    if message:
        print('[STAK] EXC  : %s' % (message % args))
    if exc:
        excType, excValue, excTb = sys.exc_info() if isPy2 else exc.__class__, exc, exc.__traceback__
        printExc(excType, excValue, excTb)
    return True

def funcErr(*_, **__):
    ERROR(
        'This noop function is here purely to avoid '
        'squiggly lines in PyCharm, which make me very nervous, '
        'but the code is supposed to fail if this is not '
        'overridden, printing callstack now.'
    )

def makeObjErr(_class):
    class ObjectError(_class): pass
    for k, v in _class.__dict__.iteritems():
        if k[:2] != '__' and callable(v):
            tryCall(setattr, ObjectError, k, funcErr)
    return ObjectError()

listErr = makeObjErr(list)
dequeErr = makeObjErr(Deque)


def getItem(accessor, accessible):
    return accessible[accessor]

getItem4 = Partial(getItem, 4)


def roundToSigFigs(x, sigFigs):
    if x == 0:
        return 0
    return round(x, sigFigs - int(floor(log10(abs(x)))) - 1)

def logExcept(func):
    @wraps(func)
    def logExceptWrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            EXCEPTION('Exception in logExcept', exc=e)

    return logExceptWrapper


def logPlaceholder(func):
    @wraps(func)
    def logPlaceholderWrapper(*args, **kwargs):
        DEBUG('Call to un-replaced placeholder: %s(%s, %s)', func.__name__, args, kwargs)
    return logPlaceholderWrapper
