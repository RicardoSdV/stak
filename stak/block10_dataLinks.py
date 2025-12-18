from .block00_autoImports import *


# Log the data passed to it next to the fist link to know where it comes from.
# ---------------------------------------------------------------------------------------------------------------------
def firstFrameAndData(locals=False, *keyValPairsForLogging, **kwargsForLogging):  # type: (...) -> None
    frame = sysGetFrame(1)
    data = tuple(serializeArgs(frame if locals else None, keyValPairsForLogging, kwargsForLogging))
    splitLink = makeSplitLink(frame, data)
    if splitLink: appendToStak((time(), (splitLink, )))

firstFrameAndDataAndLocals = Partial(firstFrameAndData, True)
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
def omrolocsoladoed(__log__, __print__, __locals__, __return__, __depth__, *keyValPairsForLog, **kwargsForLog):
    # type: (int, int, int, int, int, *Any, **Any) -> Opt[str]

    frame = sysGetFrame(__depth__)
    data = tuple(serializeArgs(frame if __locals__ else None, keyValPairsForLog, kwargsForLog))

    callChain = makeCallChain(frame, data)

    if __print__ or __return__:
        # Normally printing to std out is done for some quick logging with few entries,
        # and returning is used to print in the outer scope, so we don't care about performance.
        # That is to say, don't use this if you expect any sort of performance during logging.
        joinedChains = ' <- '.join(joinLinks(callChain))

    if __print__:
        makeSplitLinks()

    if __log__:
        stakApp(stampBF | chainBF)
        stakApp(clock())
        stakExt(callChain)

    if __return__:
        return joinedChains


# Interface:
omrolocsalad = Partial(omrolocsoladoed, 1, 0, 1, 0, 1)
omropocsalad = Partial(omrolocsoladoed, 0, 1, 1, 0, 1)
omrolocs     = Partial(omrolocsoladoed, 1, 0, 0, 0, 1)
omropocs     = Partial(omrolocsoladoed, 0, 1, 0, 0, 1)
omrorocs     = Partial(omrolocsoladoed, 0, 0, 0, 1, 2)  # When returning it is assumed that a print will provide info for the first frame.
omrolpocs    = Partial(omrolocsoladoed, 1, 1, 0, 0, 1)
# ---------------------------------------------------------------------------------------------------------------------


# Similar to _omrolocsoladoed but it's a wrapper and, it logs the return. Use the partials not this one.
# ---------------------------------------------------------------------------------------------------------------------
def _omrolocsalaraa(__log__, __print__, __locals__, __args__, __return__, __depth__, wrapable):
    # type: (int, int, int, int, int, int, Cal) -> Cal

    if __args__:
        @wraps(wrapable)
        def wrapper(*args, **kwargs):
            # TODO: Remove self and cls
            # Must serialize before calling in case of mutable args.
            strArgs = argsToStr(serializeArgs(None, args=args, kwargs=kwargs))
            returns = wrapable(*args, **kwargs)
            omrolocsoladoed(__log__, __print__, __locals__, __return__, __depth__, args=strArgs, returns=returns)
            return returns
        return wrapper

    @wraps(wrapable)
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
