from sys import _getframe

from .block00_typing                import *
from .block02_settingObj            import so
from .block05_pathOps               import pathSplitChar
from .block07_creatingMroCallChains import makeCallChain


def joinLink(
        splitLink,                # type: SplitLink
        splitChar=pathSplitChar,  # type: str
        joinB = '('.join,         # type: Join
        joinE = ''.join,          # type: Join
        joinC = ', '.join,        # type: Join
):                                # type: (...) -> str

    filePath, lineno, mroClsNs, calName, data = splitLink

    if mroClsNs and mroClsNs[-1] == 'object':
        mroClsNs = None  # If mro went all the way to object definer class never found.

    if (so.alwaysLogFilePath or not mroClsNs) and filePath:
        splitPath = filePath.split(splitChar)
        depth = so.defaultPathDepth
        if depth:
            trimPath = splitPath[-depth:]
            filePath = splitChar.join(trimPath)
        filePath = filePath[:-3]  # Remove .py
        filePath += ':'
    else:
        filePath = ''

    if (so.alwaysLogLineno or not mroClsNs) and lineno:
        lineno = '%s:' % lineno
    else:
        lineno = ''

    if mroClsNs and so.tryLogMro:
        mroClsNs = list(mroClsNs)

        depth = so.maxMroClsNsDepth
        if depth:
            mroClsNs = mroClsNs[-depth:]

        mroClsNs[-1] = '%s.%s%s' % (mroClsNs[-1], calName, ')' * (len(mroClsNs) - 1))
        mroClsNs = joinB(mroClsNs)
    elif calName:
        mroClsNs = calName
    else:
        mroClsNs = ''

    if data and so.includeData:
        data = '::[' + joinC(
            (name + '=' + strData for name, strData in data)
        ) + ']'
    else:
        data = ''

    return joinE((filePath, lineno, mroClsNs, data))

def joinLinks(splitLinks, joinLink=joinLink):  # type: (Itrb[SplitLink], ...) -> Itrt[str]
    return (joinLink(link) for link in splitLinks)

# Optional Method Resolution Order Printer Optional Call Stack
def omropocs(
        doPrint       = True,           # type: bool
        _getFrame     = _getframe,      # type: Cal[[int], FrameType]
        makeCallChain = makeCallChain,  # type: Cal[[FrameType], ...]
        joinLinks     = joinLinks,      # type: Cal[[Itrb[SplitLink], Itrt[str]]]
        join          = ' <- '.join     # type: Join
):                                       # type: (...) -> str
    frame = _getFrame(1)
    strLink = join(joinLinks(makeCallChain(frame)))
    if doPrint: print 'OMROPOCS: ' + strLink
    return strLink
