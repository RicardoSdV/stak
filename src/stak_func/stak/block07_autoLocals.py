from sys import _getframe
from time import time

from .block00_typing import *
from .block02_commonData import dataFlag
from .block03_log import appendToLog, extendLog
from .block06_creatingMroCallChains import jointLinkFromFrame, omrolocs


def joinStrLinkWithDataForLogging(pretty, strLink, flag=dataFlag, **dataForLogging):  # type: (bool, str, str, Any) -> None
    if pretty and len(dataForLogging) > 2:
        now = time()

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
                flag,
                (
                    '{}('.format(strLink) +
                    ', '.join(('{}={}'.format(name, datum) for name, datum in dataForLogging.iteritems())) +
                    ')'
                ) if dataForLogging else strLink + '(No data was passed)'
            )
        )


def dataAndFirstFrame(pretty=True, **dataForLogging):  # type: (bool, Any) -> None
    """ Log data structures, their callable & definer class names """
    joinStrLinkWithDataForLogging(
        pretty,
        jointLinkFromFrame(_getframe(1)),
        **dataForLogging
    )

def autoLocals(frameNum=1, silence=False, pretty=False, **additionalDataForLogging):
    # type: (int, bool, bool, Any) -> None
    """ Logs locals from frame from which this method was called, optionally other kwargs """
    if silence: return

    firstFrame = _getframe(frameNum)
    for key, value in firstFrame.f_locals.iteritems():
        if key != 'self' and key != 'cls':
            additionalDataForLogging[key] = value

    joinStrLinkWithDataForLogging(
        pretty,
        jointLinkFromFrame(firstFrame),
        **additionalDataForLogging
    )

def omrolocsalad(silence=False, pretty=False, **additionalDataForLogging): # type: (bool, bool, Any) -> None
    """ Call omrolocs & autoLocals at the same time """
    if silence: return
    omrolocs(2, silence)
    autoLocals(2, silence, pretty, **additionalDataForLogging)
