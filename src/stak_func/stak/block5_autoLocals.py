from os.path import join
from sys import _getframe
from time import time
from types import ClassType as OldStyleClsType

from .block1_commonData import *
from .block4_creatingMroCallChains import privInsMethCond, privClsMethCond, mroClsNsGen, pubInsMethCond, pubClsMethCond, pathSplitChar
from .block9_savingAllLogs import mroLinkToStrLink


def data(pretty, strLink, **dataForLogging):  # type: (bool, str, Any) -> None
    if pretty:
        now, flag = time(), stakFlags[2]

        if dataForLogging:
            appendToLog((now, flag, '{}('.format(strLink)))
            extendLog(
                (now, flag, '    {}={},'.format(name, datum))
                for name, datum in dataForLogging.iteritems()
            )
            appendToLog((now, flag, ')'))
    else:
        appendToLog(
            (
                time(),
                stakFlags[2],
                (
                    '{}('.format(strLink) +
                    ', '.join(('{}={}'.format(name, datum) for name, datum in dataForLogging.iteritems())) +
                    ')'
                ) if dataForLogging else '{}('.format(strLink) + 'No data was passed)'
            )
        )

def linksAndFirstFrameLocalsFromFrame():  # type: () -> Itrt[Uni[Dic[str, Any], Tup[Lst[str], str], Tup[str, int, str]]]
    frame = _getframe(2)
    codeObj, fLocals = frame.f_code, frame.f_locals
    methName = codeObj.co_name
    yield fLocals

    while True:
        callerCls = None
        if 'self' in fLocals:
            callerCls = fLocals['self'].__class__
            defClsCond = privInsMethCond if methName.startswith('__') and not methName.endswith('__') else pubInsMethCond
        elif 'cls' in fLocals:
            callerCls = fLocals['cls']
            defClsCond = privClsMethCond if methName.startswith('__') and not methName.endswith('__') else pubClsMethCond

        if callerCls is None or isinstance(callerCls, OldStyleClsType):
            yield codeObj.co_filename, frame.f_lineno, methName
        else:
            # PyCharm thinks defClsCond could be undefined, but if callerCls is not None it must be defined
            mroClsNs = list(mroClsNsGen(callerCls, defClsCond, methName, codeObj))
            if mroClsNs[-1] == 'object':  # Sometimes definer class not found so follow inheritance tree to the root
                yield codeObj.co_filename, frame.f_lineno, methName
            else:
                yield mroClsNs, methName

        frame = frame.f_back
        if not frame: break
        codeObj, fLocals = frame.f_code, frame.f_locals
        methName = codeObj.co_name

def splitLinkToStr(splitLink):  # type: (Uni[Tup[Lst[str], str], Tup[str, int, str]]) -> str
    # REMINDER: Always add \n at the last possible moment, it's been tried before, it does not work!
    if len(splitLink) == 3:
        filePath, lineno, methName = splitLink
        splitFilePath = filePath.split(pathSplitChar)
        if len(splitFilePath) > 1:
            return '{}{}.{}'.format(join(splitFilePath[-2], splitFilePath[-1]).rstrip('py'), lineno, methName)
        else:
            return '{}{}.{}'.format(join(splitFilePath[-1]).rstrip('py'), lineno, methName)
    else:
        return mroLinkToStrLink(*splitLink)

