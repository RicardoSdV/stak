from .block00_autoImports import *

def stampToStr(stamp):
    return 'stamp-to-str-not-implemented'


def joinLink(iterLinks, ): pass


def joinLinks(iterLinks, _mroLink = mroLinkEntry, _strByHash = jointLinks_strByPathLnHash):
    for flag in iterLinks:
        filePath = next(iterLinks)
        lineno = next(iterLinks)
        calName = next(iterLinks)
        if flag == _mroLink:
            cnt = next(iterLinks)
            mroClsNs = list(islice(iterLinks, cnt))
        else:
            mroClsNs = None

        linkHash = hash((filePath, lineno))
        if linkHash in _strByHash:
            return _strByHash[linkHash]

        strLink = ''

        if alwaysLogFilePath or not mroClsNs:
            if defaultPathDepth:
                filePath = pathSplitChar.join(filePath.split(pathSplitChar)[-defaultPathDepth:])
            strLink += filePath[:-3]  # Remove .py
            strLink += ':'

        if alwaysLogLineno or not mroClsNs:
            strLink += '%s:' % lineno

        if mroClsNs and tryLogMro:
            if maxMroClsNsDepth:
                mroClsNs = mroClsNs[-maxMroClsNsDepth:]
            mroClsNs[-1] = '%s.%s%s' % (mroClsNs[-1], calName, ')' * (len(mroClsNs) - 1))
            strLink += '('.join(mroClsNs)
        else:
            strLink += calName

        _strByHash[linkHash] = strLink
        return strLink


def getJointLink(linkHash, _strByHash = jointLinks_strByPathLnHash, _headByHash=splitLinks_headIdxByPathLnHash):
    if linkHash in _strByHash:
        return _strByHash[linkHash]

    head = _headByHash[linkHash]
    iterLinks = islice(splitLinks, head, len(splitLinks))
    strLink = joinLinks(iterLinks)
    return strLink


def joinLinksByHashes(linkHashes):  # type: (Itrb[int]) -> Lst[str]
    return [getJointLink(linkHash) for linkHash in linkHashes]

def joinKVData(iterData):  # type: (Itrt[str]) -> str
    strData = '::['
    for k in iter(iterData):
        strData += k + next(iterData) + ', '
    return strData[:-2] + '] '


def joinChains(callChains):
    iterChains = iter(callChains)

    jointChains = []
    jointChainsApp = jointChains.append

    for flag in iterChains:
        if flag == callChainEntry:
            stamp = next(iterChains)
            linkCnt = next(iterChains)
            iterHashes = islice(iterChains, linkCnt)
            yield stampToStr(stamp) + ' <- '.join(joinLinksByHashes(iterHashes))

        elif flag == dataChainEntry:
            # TODO: figure out what to do with data so that data chains can get compressed too.

            stamp = next(iterChains)
            dataCnt = next(iterChains)
            data = islice(iterChains, dataCnt)
            strData = joinKVData(data)
            linkCnt = next(iterChains)
            iterHashes = islice(iterChains, linkCnt)
            yield stampToStr(stamp) + ' <- '.join(joinLinksByHashes(iterHashes))

        elif flag == labelEntry:
            yield next(iterChains)

        elif flag == dateEntry:
            # TODO: I need the actual time given by time and the precision of clock somehow.
            timeStamp = next(iterChains)
            clockStamp = next(iterChains)

        else:
            raise ValueError('Unknown flag = %s' % flag)











def joinLinkOG(
        splitLink,                # type: Itrt[Uni[str, int, float]]
        joinB = '('.join,         # type: Join
        joinE = ''.join,          # type: Join
        joinC = ', '.join,        # type: Join
):                                # type: (...) -> str

    try:
        filePath, lineno, mroClsNs, calName, data = splitLink
    except:
        filePath, lineno, mroClsNs, calName, data, _ = splitLink  # TODO: Quick hack to print traces for debugging self, fix!!!!!!!


    if mroClsNs and mroClsNs[-1] == 'object':
        mroClsNs = None  # If mro went all the way to object definer class never found.

    if (alwaysLogFilePath or not mroClsNs) and filePath:
        splitPath = filePath.split(pathSplitChar)
        depth = defaultPathDepth
        if depth:
            trimPath = splitPath[-depth:]
            filePath = pathSplitChar.join(trimPath)
        filePath = filePath[:-3]  # Remove .py
        filePath += ':'
    else:
        filePath = ''

    if (alwaysLogLineno or not mroClsNs) and lineno:
        lineno = '%s:' % lineno
    else:
        lineno = ''

    if mroClsNs and tryLogMro:
        mroClsNs = list(mroClsNs)

        depth = maxMroClsNsDepth
        if depth:
            mroClsNs = mroClsNs[-depth:]

        mroClsNs[-1] = '%s.%s%s' % (mroClsNs[-1], calName, ')' * (len(mroClsNs) - 1))
        mroClsNs = joinB(mroClsNs)
    elif calName:
        mroClsNs = calName
    else:
        mroClsNs = ''

    if data and includeData:
        data = '::[' + joinC(
            (name + '=' + strData for name, strData in data)
        ) + ']'
    else:
        data = ''

    return joinE((filePath, lineno, mroClsNs, data))
