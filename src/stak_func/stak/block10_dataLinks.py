from functools import partial
from itertools import izip
from sys import _getframe
from time import time

from .block00_typing import *
from .block04_log import appendToLog
from .block08_creatingMroCallChains import makeSplitLink, makeCallChain


def getStrData(frame, pairsData, dictData, exclFromLocals={'self', 'cls'}, zip=izip):  # type: (Opt[FrameType], Tup[Any, ...], Dic[str, Any], Set[str], Zip) -> Itrt[Tup[str, str]]
    """ If frame get locals from it too """

    for k, v in zip(pairsData):
        yield str(k), str(v)

    for k, v in dictData.iteritems():
        yield k, str(v)

    if not frame:
        return

    for k, v in frame.f_locals.iteritems():
        if k not in exclFromLocals and k not in dictData:
            yield k, str(v)

def firstFrameAndData(locals=False, *keyValPairsForLogging, **kwargsForLogging):  # type: (bool, *Any, **Any) -> None
    """ Log the data passed to it next to the fist link to know where it comes from. """

    frame = _getframe(1)
    data = tuple(getStrData(frame if locals else None, keyValPairsForLogging, kwargsForLogging))
    appendToLog((time(), (makeSplitLink(frame, data), )))

firstFrameAndDataAndLocals = partial(firstFrameAndData, True)


def omrolocsalad(*keyValPairsForLog, **kwargsForLog):  # type: (*Any, **Any) -> None
    """
    Logs locals of frame from which this method was called & the call chain with the mro if it can be found,

    Extra data that passed as:
        keyValPairsForLogging: So that str keys can be passed & order is kept, one key followed by one val
        kwargsForLogging: For when keys can be regular key-words.
    """

    frame = _getframe(1)
    data = tuple(getStrData(frame, keyValPairsForLog, kwargsForLog))
    callChain = tuple(makeCallChain(frame, data))
    appendToLog((time(), callChain))
