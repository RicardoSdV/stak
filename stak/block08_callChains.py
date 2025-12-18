from .block00_autoImports import *

# For some reason instance methods are FunctionType, at runtime, but not when testing
# them out in the console, so isinstance(method, MethodType) is False at runtime, but
# True in the console, so, yeah, what's going on there?

def makeMroClsNs(frame):  # type: (Frame) -> Opt[Lst[str]]
    """ mroClsNs = (callerCls, ..., mroClasses, ..., definerCls) """
    fLocals = frame.f_locals

    if 'self' in fLocals:
        callerCls = fLocals['self'].__class__
        isIns = True
    elif 'cls' in fLocals:
        callerCls = fLocals['cls']
        isIns = False
    else:
        return None

    if not isinstance(callerCls, type):
        return None  # Old style classes not supported

    mro = callerCls.__mro__
    if not mro:
        return None

    mroClsNs = []; mroClsNsApp = mroClsNs.append
    codeObjToFindDefClsOf = frame.f_code
    calName = codeObjToFindDefClsOf.co_name
    isPriv = calName[:2] == '__' and calName[-2:] != '__'

    for cls in mro:
        mroClsNsApp(cls.__name__)

        mangledMaybeName = '_' + cls.__name__.rstrip('_') + calName if isPriv else calName
        if mangledMaybeName not in cls.__dict__:
            continue

        clsAttr = cls.__dict__[mangledMaybeName]
        if isinstance(clsAttr, property):
            if getattr(clsAttr.fget, '__code__', None) is codeObjToFindDefClsOf: return mroClsNs
            if getattr(clsAttr.fset, '__code__', None) is codeObjToFindDefClsOf: return mroClsNs
            if getattr(clsAttr.fdel, '__code__', None) is codeObjToFindDefClsOf: return mroClsNs
            continue

        if isIns:
            if isinstance(clsAttr, Function) and clsAttr.__code__ is codeObjToFindDefClsOf:
                return mroClsNs
        else:
            if isinstance(clsAttr, classmethod) and clsAttr.__func__.__code__ is codeObjToFindDefClsOf:
                return mroClsNs

    # If we exhaust the mro we haven't found the definer class. So, we return None, in case this bug
    # should be fixed return here the entire mro & post process, or fix this function. I'm not sure why
    # there's edge cases where the class is not found.
    return None

def makeSplitLink(frame, _hash=hash, _headByHash=splitLinks_headIdxByPathLnHash):
    codeObj = frame.f_code
    path = codeObj.co_filename
    lineno = frame.f_lineno
    _hash = _hash((path, lineno))
    if _hash in _headByHash:
        return _hash

    mroClsNs = makeMroClsNs(frame)
    flag = mroLinkEntry if mroClsNs else fileLinkEntry
    splitLink = [flag, path, lineno, codeObj.co_name]
    if mroClsNs:
        splitLink.append(len(mroClsNs))
        splitLink.extend(mroClsNs)

    headIdx = len(splitLinks)
    splitLinksExt(splitLink)
    _headByHash[_hash] = headIdx
    return _hash

def getSplitLink(linkHash, _head=splitLinks_headIdxByPathLnHash, _splitLinks=splitLinks, _len=baseEntryLens, _cntIdxs=cntIdxsByEntryFlag):
    _head = _head[linkHash]
    flag = _splitLinks[_head]
    _len = _len[flag]
    for cntIdx in _cntIdxs[flag]:
        _len += _splitLinks[cntIdx]
    return _splitLinks[_head : _head + _len]


def makeCallChain(frame, entryData=None, _clock=clock):
    if entryData:
        callChain = [dataChainEntry, _clock(), len(entryData)]
        callChain.extend(entryData)
    else:
        callChain = [callChainEntry, _clock()]

    callChainApp = callChain.append
    linkCntIdx = len(callChain)
    callChainApp(None)

    while frame:
        linkHash = makeSplitLink(frame)
        callChainApp(linkHash)
        frame = frame.f_back

    callChain[linkCntIdx] = len(callChain) - linkCntIdx - 1
    return callChain
