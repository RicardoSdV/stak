from sys import _getframe
from time import time

from .block00_typing import *
from .block03_commonData import daffFlag, defaultSegFlag
from .block05_log import appendToLog, extendLog
from .block08_flagOps import getSegFlag
from .block09_creatingMroCallChains import jointLinkFromFrame, omrolocs


def joinStrLinkWithDataForLogging(
        pretty,                  # type: bool
        strLink,                 # type: str
        segFlag=defaultSegFlag,  # type: str
        callFlag=daffFlag,       # type: str
        **dataForLogging         # type: Any
):                               # type: (...) -> None

    if pretty and len(dataForLogging) > 2:
        now = time()

        if dataForLogging:
            appendToLog((now, segFlag, callFlag, '{}('.format(strLink)))
            extendLog(
                (now, segFlag, callFlag, '    {}={},'.format(name, datum))
                for name, datum in dataForLogging.iteritems()
            )
            appendToLog((now, segFlag, callFlag, ')'))
    else:
        appendToLog(
            (
                time(), segFlag, callFlag,
                (
                    '{}('.format(strLink) +
                    ', '.join(('{}={}'.format(name, datum) for name, datum in dataForLogging.iteritems())) +
                    ')'
                ) if dataForLogging else strLink + '(No data was passed)'
            )
        )

def dataAndFirstFrame(pretty=True, frame=_getframe, getFlag=getSegFlag, **dataForLogging):
    # type: (bool, Cal[[int], FrameType], Cal[[FrameType], str],  Any) -> None
    """ Log the data passed to it next to the fist link to know where it comes from. """
    frame = frame(1)
    joinStrLinkWithDataForLogging(
        pretty,
        jointLinkFromFrame(frame),
        getFlag(frame),
        **dataForLogging
    )

def autoLocals(frameNum=1, pretty=False, frame=_getframe, getFlag=getSegFlag, **additionalDataForLogging):
    # type: (int, bool, Cal[[int], FrameType], Cal[[FrameType], str], Any) -> None
    """ Logs locals from frame from which this method was called, optionally other kwargs """

    frame = frame(frameNum)
    for key, value in frame.f_locals.iteritems():
        if key != 'self' and key != 'cls':
            additionalDataForLogging[key] = value

    joinStrLinkWithDataForLogging(
        pretty,
        jointLinkFromFrame(frame),
        getFlag(frame),
        **additionalDataForLogging
    )

def omrolocsalad(pretty=False, **additionalDataForLogging): # type: (bool, Any) -> None
    """ Call omrolocs & autoLocals at the same time: Optional Method Resolution Order Logger Optional Call Stack And Locals Auto Data """
    omrolocs(2)
    autoLocals(2, pretty, **additionalDataForLogging)
