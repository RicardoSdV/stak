
from .chains import makeDataEntry, makeCallChainEntry
from ..lib import sysGetFrame, Partial, funcToolsWraps
from ..state import stakLogExt
from ..utils.serial import serializeArgs, argsToStr
from ..utils.exc import logExcept


# Log the data passed to it next to the fist link to know where it comes from.
# ---------------------------------------------------------------------------------------------------------------------
@logExcept
def firstFrameAndData(__log__, __print__, __locals__, __return__, __depth__, *keyValPairsForLogging, **kwargsForLogging):  # type: (...) -> None
    if not keyValPairsForLogging and not kwargsForLogging:
        return
    dataEntry = makeDataEntry(sysGetFrame(1) if __locals__ else None, keyValPairsForLogging, kwargsForLogging)
    stakLogExt(dataEntry)

    # TODO: Print data entry?

firstFrameAndDataAndLocals = Partial(firstFrameAndData, True)
# ---------------------------------------------------------------------------------------------------------------------


# Optional Method Resolution Order Logger Optional Callstack Optional Locals Auto Data Optional Extra Data.
#
# __log__   : If True, will add entry to log in RAM for formatting & saving later on.
#
# __print__ : If True, will print formatted entry
#
# __locals__: If True, logs locals from frame from which it was called.
#
# __return__: If True, returns formatted entry for processing in the outer scope
#
# __depth__ : Int to understand what frame we should start at in the call chain, take locals from, etc.
#
# Extra data that passed as:
#     - keyValPairsForLogging: So that str keys can be passed & order is kept, one key followed by
#       one val, unless it's the last key-val pair and then the key can be the value.
#
#     - kwargsForLogging: For when keys can be regular key-words & you don't care about order.
# ---------------------------------------------------------------------------------------------------------------------
@logExcept
def omrolocsoladoed(__log__, __print__, __locals__, __return__, __depth__, *keyValPairsForLog, **kwargsForLog):
    frame = sysGetFrame(__depth__)

    if keyValPairsForLog or kwargsForLog or __locals__:
        data = tuple(serializeArgs(frame if __locals__ else None, keyValPairsForLog, kwargsForLog))
        callChainEntry = makeCallChainEntry(frame, data)
    else:
        callChainEntry = makeCallChainEntry(frame)

    if __print__ or __return__:
        # Normally printing to std out is done for some quick logging with few entries,
        # & returning is used to print in the outer scope, so we don't care about performance.
        # That is to say, don't use this if you expect any sort of performance during logging.
        jointCallChainEntry = ' <- '.join(joinLinks(callChainEntry))

    if __print__:
        print(jointCallChainEntry)

    if __log__:
        stakLogExt(callChainEntry)

    if __return__:
        return jointCallChainEntry


# Interface:
omrolocsalad = Partial(omrolocsoladoed, 1, 0, 1, 0, 1)
omropocsalad = Partial(omrolocsoladoed, 0, 1, 1, 0, 1)
omrolocs     = Partial(omrolocsoladoed, 1, 0, 0, 0, 1)
omropocs     = Partial(omrolocsoladoed, 0, 1, 0, 0, 1)
omrorocs     = Partial(omrolocsoladoed, 0, 0, 0, 1, 2)  # When returning it is assumed that a print will provide info for the first frame.
omrolpocs    = Partial(omrolocsoladoed, 1, 1, 0, 0, 1)
# ---------------------------------------------------------------------------------------------------------------------


# Similar to _omrolocsoladoed but it's a wrapper & logs the return. Use the partials not this one.
# ---------------------------------------------------------------------------------------------------------------------
@logExcept
def _omrolocsalaraa(__log__, __print__, __locals__, __args__, __return__, __depth__, wrapable):
    # type: (int, int, int, int, int, int, Cal) -> Cal

    if __args__:
        @funcToolsWraps(wrapable)
        def wrapper(*args, **kwargs):
            # Must serialize before calling in case of mutable args.
            strArgs = argsToStr(serializeArgs(None, args=args, kwargs=kwargs))
            returns = wrapable(*args, **kwargs)
            omrolocsoladoed(__log__, __print__, __locals__, __return__, __depth__, args=strArgs, returns=returns)
            return returns
        return wrapper

    @funcToolsWraps(wrapable)
    def wrapper(*args, **kwargs):
        returns = wrapable(*args, **kwargs)
        omrolocsoladoed(__log__, __print__, __locals__, __return__, __depth__, returns=returns)
        return returns
    return wrapper

omrolocsalar = Partial(_omrolocsalaraa, 1, 0, 1, 1, 0)
omropocsalar = Partial(_omrolocsalaraa, 0, 1, 1, 1, 0)
omrolocsar   = Partial(_omrolocsalaraa, 1, 0, 0, 0, 0)
omropocsar   = Partial(_omrolocsalaraa, 0, 1, 0, 0, 0)
# ---------------------------------------------------------------------------------------------------------------------
