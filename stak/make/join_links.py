from ..config import alwaysLogFilePath, defaultPathDepth
from ..const import mroLinkEntryFlag, callChainEntryFlag, dataChainEntryFlag, labelEntryFlag
from ..lib import iSlice, dtFromTimeStamp
from ..state import config, splitLinksById, jointLinksById
from ..utils.paths import pathSplitChar


def stampToStr(stamp):
    return 'stamp-to-str-not-implemented'


def joinLink(splitLink):
    iterLink = iter(splitLink)

    flag = next(iterLink)
    filePath = next(iterLink)
    lineno = next(iterLink)
    calName = next(iterLink)

    if flag == mroLinkEntryFlag:
        cnt = next(iterLink)
        mroClsNs = list(iSlice(iterLink, cnt))
    else:
        mroClsNs = None

    strLink = ''

    if alwaysLogFilePath or not mroClsNs:
        if defaultPathDepth:
            filePath = pathSplitChar.join(filePath.split(pathSplitChar)[-defaultPathDepth:])
        strLink += filePath[:-3]  # Remove .py
        strLink += ':'

    if config['alwaysLogLineno'] or not mroClsNs:
        strLink += '%s:' % lineno

    if mroClsNs and config['tryLogMro']:
        if config['maxMroClsNsDepth']:
            mroClsNs = mroClsNs[-config['maxMroClsNsDepth']:]
        mroClsNs[-1] = '%s.%s%s' % (mroClsNs[-1], calName, ')' * (len(mroClsNs) - 1))
        strLink += '('.join(mroClsNs)
    else:
        strLink += calName

    return strLink

def joinAllLinks():
    for _id, splitLink in enumerate(splitLinksById):
        if _id in jointLinksById:
            continue

        jointLink = joinLink(splitLink)
        jointLinksById[_id] = jointLink


def joinKVData(iterData):
    strData = '::['
    for k in iter(iterData):
        strData += k + next(iterData) + ', '
    return strData[:-2] + '] '


def joinStakLogEntries(log):
    """ This func can join all the entries in stakLog or a subsection if
    sliced in the right places can be joined too. """
    joinAllLinks()

    iterLog = iter(log)

    jointLog = []
    jointLogApp = jointLog.append

    for flag in iterLog:
        if flag == callChainEntryFlag:
            stamp = next(iterLog)
            linkCnt = next(iterLog)
            iterHashes = iSlice(iterLog, linkCnt)
            yield stampToStr(stamp) + 'TODO: '  # <- '.join(joinLinksByHashes(iterHashes))

        elif flag == dataChainEntryFlag:
            # TODO: figure out what to do with data so that data chains can get compressed too.

            stamp = next(iterLog)
            dataCnt = next(iterLog)
            data = iSlice(iterLog, dataCnt)
            strData = joinKVData(data)
            linkCnt = next(iterLog)
            iterHashes = iSlice(iterLog, linkCnt)
            yield stampToStr(stamp) + 'TODO: '  # ' <- '.join(joinLinksByHashes(iterHashes))

        elif flag == labelEntryFlag:
            stamp = next(iterLog)
            label = next(iterLog)
            yield stampToStr(stamp) + label

        elif flag == 'TODO: Date entries':
            absStamp = next(iterLog)
            clockStamp = next(iterLog)
            yield dtFromTimeStamp(absStamp).strftime('%Y-%m-%d')

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

    if (config['alwaysLogLineno'] or not mroClsNs) and lineno:
        lineno = '%s:' % lineno
    else:
        lineno = ''

    if mroClsNs and config['tryLogMro']:
        mroClsNs = list(mroClsNs)

        depth = config['maxMroClsNsDepth']
        if depth:
            mroClsNs = mroClsNs[-depth:]

        mroClsNs[-1] = '%s.%s%s' % (mroClsNs[-1], calName, ')' * (len(mroClsNs) - 1))
        mroClsNs = joinB(mroClsNs)
    elif calName:
        mroClsNs = calName
    else:
        mroClsNs = ''

    if data and config['includeData']:
        data = '::[' + joinC(
            (name + '=' + strData for name, strData in data)
        ) + ']'
    else:
        data = ''

    return joinE((filePath, lineno, mroClsNs, data))
