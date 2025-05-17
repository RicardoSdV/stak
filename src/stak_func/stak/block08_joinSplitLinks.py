from sys import _getframe

from .block00_typing import *
from .block02_settingObj import so
from .block05_pathOps import pathSplitChar
from .block07_creatingMroCallChains import makeCallChain


def joinLink(splitLink, splitChar=pathSplitChar):  # type: (SplitLink, str) -> str
    filePath, lineno, mroClsNs, calName, data = splitLink

    if mroClsNs and mroClsNs[-1] == 'object':
        mroClsNs = None  # If mro went all the way to object definer class never found.

    if so.alwaysLogFilePath or not mroClsNs:
        splitPath = filePath.split(splitChar)
        depth = so.defaultPathDepth
        if depth:
            trimPath = splitPath[-depth:]
            filePath = splitChar.join(trimPath)
        filePath = filePath[:-3]  # Remove .py
        filePath += ':'
    else:
        filePath = ''

    if so.alwaysLogLineno or not mroClsNs:
        lineno = '%s:' % lineno
    else:
        lineno = ''

    if mroClsNs and so.tryLogMro:
        mroClsNs = list(mroClsNs)

        depth = so.maxMroClsNsDepth
        if depth:
            mroClsNs = mroClsNs[-depth:]

        mroClsNs[-1] = '%s.%s%s' % (mroClsNs[-1], calName, ')' * (len(mroClsNs) - 1))
        mroClsNs = '('.join(mroClsNs)
    else:
        mroClsNs = calName

    if data and so.includeData:
        splitData = []
        append = splitData.append

        for name, strData in data:
            append(name + '=' + strData)

        data = '::[' + ', '.join(splitData) + ']'
    else:
        data = ''

    return filePath + lineno + mroClsNs + data

def joinLinks(splitLinks, join=joinLink):  # type: (Itrb[SplitLink], ...) -> Itrt[str]
    return (join(link) for link in splitLinks)

# Optional Method Resolution Order Printer Optional Call Stack
def omropocs(
        doPrint        = True,           # type: bool
        _getFrame      = _getframe,      # type: Cal[[int], FrameType]
        _makeCallChain = makeCallChain,  # type: Cal[[FrameType], ...]
        _joinLinks     = joinLinks,      # type: Cal[[Itrb[SplitLink], Itrt[str]]]
):                                       # type: (...) -> None
    frame = _getFrame(1)
    strLink = ' <- '.join(_joinLinks(_makeCallChain(frame)))
    if doPrint: print 'OMROPOCS: ' + strLink
    return strLink
