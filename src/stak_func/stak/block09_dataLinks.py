from functools import partial, wraps
from sys       import _getframe
from time      import time

from .block00_typing     import *
from .block04_log        import appendToStak
from .block07_callChains import makeSplitLink, makeCallChain
from .block08_joinLinks  import joinLinks
from .block15_utils      import serializeArgs, argsToStr


# Log the data passed to it next to the fist link to know where it comes from.
# ---------------------------------------------------------------------------------------------------------------------
def firstFrameAndData(locals=False, _makeSplitLink=makeSplitLink, _getFrame=_getframe, *keyValPairsForLogging, **kwargsForLogging):                                       # type: (...) -> None
    frame = _getframe(1)
    data = tuple(serializeArgs(frame if locals else None, keyValPairsForLogging, kwargsForLogging))
    splitLink = _makeSplitLink(frame, data)
    if splitLink: appendToStak((time(), (splitLink, )))

firstFrameAndDataAndLocals = partial(firstFrameAndData, True)
# ---------------------------------------------------------------------------------------------------------------------


# Optional Method Resolution Order Optional Callstack Optional Locals Auto Data Optional Extra Data.
#
# __print__: To decide weather to print or append
#
# __locals__: If true logs locals from frame from which it was called.
#
# Extra data that passed as:
#     - keyValPairsForLogging: So that str keys can be passed & order is kept, one key followed by
#       one val, unless it's the last key-val pair and then the key can be the value.
#
#     - kwargsForLogging: For when keys can be regular key-words & you don't care about order.
# ---------------------------------------------------------------------------------------------------------------------
def _omrolocsoladoed(__print__, __locals__, __depth__ = 1, *keyValPairsForLog, **kwargsForLog):
    # type: (bool, bool, int, *Any, **Any) -> None

    frame = _getframe(__depth__)
    data = tuple(serializeArgs(frame if __locals__ else None, keyValPairsForLog, kwargsForLog))
    callChain = tuple(makeCallChain(frame, data))

    if __print__:
        print ' <- '.join(joinLinks(callChain))
    else:
        appendToStak((time(), callChain))

omrolocsalad = partial(_omrolocsoladoed, False, True , 1)
omropocsalad = partial(_omrolocsoladoed, True , True , 1)
omrolocs     = partial(_omrolocsoladoed, False, False, 1)
omropocs     = partial(_omrolocsoladoed, True , False, 1)
# ---------------------------------------------------------------------------------------------------------------------


# Similar to _omrolocsoladoed but it's a wrapper and, it logs the return. Use the partials not this one.
# ---------------------------------------------------------------------------------------------------------------------
def _omrolocsalaraa(__print__, __locals__, __args__, wrapable):
    # type: (bool, bool, bool, Cal) -> Cal

    if __args__:
        @wraps(wrapable)
        def wrapper(*args, **kwargs):
            # TODO: Remove self and cls
            # Must serialize before calling in case of mutable args.
            strArgs = argsToStr(serializeArgs(None, args=args, kwargs=kwargs))
            returns = wrapable(*args, **kwargs)
            _omrolocsoladoed(__print__, __locals__, 2, args=strArgs, returns=returns)
            return returns
        return wrapper

    @wraps(wrapable)
    def wrapper(*args, **kwargs):
        returns = wrapable(*args, **kwargs)
        _omrolocsoladoed(__print__, __locals__, 2, returns=returns)
        return returns
    return wrapper

omrolocsalar = partial(_omrolocsalaraa, False, True , True)
omropocsalar = partial(_omrolocsalaraa, True , True , True)
omrolocsar   = partial(_omrolocsalaraa, False, False, False)
omropocsar   = partial(_omrolocsalaraa, True , False, False)
# ---------------------------------------------------------------------------------------------------------------------

