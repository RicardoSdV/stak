from .block00_autoImports import *

red = 31
grey = 90

def colorStr(code, _str):
    return '\033[{code}m{_str}\033[0m'.format(code=code, _str=_str)

def tryCall(_callable, *args, **kwargs):  # type: (Cal, *Any, **Any) -> Any
    errMess = kwargs.pop('errMess', None)
    try:
        return _callable(*args, **kwargs)
    except Exception as e:
        if errMess: E(errMess, exception=formatExc())
        else      : E(exception=formatExc())

def serializeArgs(frame, args, kwargs):
    # type: (Opt[FrameType], Tup[Any, ...], Dic[str, Any]) -> Itrt[Tup[str, str]]

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
    if printStack: printStack()
    print colorStr(color, mess)

P = Partial(LOG, '[PRINT]', grey, False)
E = Partial(LOG, '[ERROR]', red , True )


def funcErr(*_, **__):
    print ('ERROR: This noop function is here purely to avoid '
           'squiggly lines in PyCharm, which make me very nervous, '
           'but the code is supposed to fail if this is not '
           'overridden, printing callstack now.')
    printStack()
    return

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


def printTestSetting():
    print testSetting
