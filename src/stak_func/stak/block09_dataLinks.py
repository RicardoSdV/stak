from functools import partial
from sys import _getframe
from time import time

from .block00_typing import *
from .block04_log import appendToStak
from .block07_creatingMroCallChains import makeSplitLink, makeCallChain
from .z_utils import serializeArgs

# Log the data passed to it next to the fist link to know where it comes from.
# -------------------------------------------------------------------------------------------------
def firstFrameAndData(locals=False, _makeSplitLink=makeSplitLink, _getFrame=_getframe, *keyValPairsForLogging, **kwargsForLogging):                                       # type: (...) -> None
    frame = _getframe(1)
    data = tuple(serializeArgs(frame if locals else None, keyValPairsForLogging, kwargsForLogging))
    splitLink = _makeSplitLink(frame, data)
    if splitLink: appendToStak((time(), (splitLink, )))

firstFrameAndDataAndLocals = partial(firstFrameAndData, True)


# Logs locals of frame from which this method was called & the call
# chain with the mro if it can be found.
#
# Extra data that passed as:
#     - keyValPairsForLogging: So that str keys can be passed & order is kept, one key followed by
#       one val, unless it's the last key-val pair and then the key can be the value.
#
#     - kwargsForLogging: For when keys can be regular key-words & you don't care about order.
# -------------------------------------------------------------------------------------------------
def omrolocsalad(*keyValPairsForLog, **kwargsForLog):  # type: (*Any, **Any) -> None
    frame = _getframe(1)
    data = tuple(serializeArgs(frame, keyValPairsForLog, kwargsForLog))
    callChain = tuple(makeCallChain(frame, data))
    appendToStak((time(), callChain))
