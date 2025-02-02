from datetime import datetime
from time import time

from .block00_typing import *
from .block01_settings import eventLabels
from .block03_commonData import labelFlag, dateFlag, defaultSegFlag
from .block06_pathOps import getStdLogPaths


class Log(list):
    def __init__(self, *args):
        super(Log, self).__init__(args)
        self.eventCnt = 0

def clearLog():
    """ DANGER: Clears current logs, stak & std. Resets eventCnt (label print count) & more """
    for path in getStdLogPaths():
        with open(path, 'w') as _: pass

    log.eventCnt = 0
    log[:] = []
    dateEntry()

def labelLog(label=None):  # type: (Opt[str]) -> None
    """ Make a log entry with the passed label, else, with next label in eventLabels, if any, else print no-name label """

    if label is None:
        if log.eventCnt < len(eventLabels):
            label = eventLabels[log.eventCnt]
        else:
            label = 'NO-NAME LABEL' + str(len(eventLabels) - log.eventCnt)
        log.eventCnt += 1

    appendToLog(
        (
            time(),
            labelFlag,
            '\n========================================================= {} '
            '=========================================================\n'.format(label)
        )
    )

def dateEntry():
    """ Since normal entries only log time, this one is used to log date, normally on logging session init. """
    appendToLog((time(), defaultSegFlag, dateFlag, datetime.now().strftime('%Y-%m-%d')))


log = Log()  # type: Log[Tup[float, str, str, Uni[Tup[SplitLink, ...], str]]]
appendToLog = log.append
extendLog   = log.extend
dateEntry()

traceLog = []  # type: Lst[Tup[float, str, SplitLink]]
appendToTrace = traceLog.append

"""
log = [
    (unixStamp, seggregatorFlag, callerFlag, theRest),
]

theRest = fileLink OR mroLink OR customStringEntry

fileLink = (path, lineno, methName)

mroLink = (classMRO, methName)

classMRO = [callerCls, ..., mroClasses, ..., definerCls]

callerCls -> the class which was instantiated to call the method

definerCls -> the class in which the method is defined

mroClasses -> all the classes following the MRO from the callerCls up to the definerCls (might not be any)

(caller & definer classes might be the same, in which case theres only one element in the list)

seggregatorFlag -> A flag used to divide up logs, it's "main" by default & can be modified when importing stak
                    to any custom flag
                    
callerFlag -> Mainly used for log post-processing, loosely represents the method which was called to make the 
                given log entry.
                
customStringEntry -> For supporting entries such as date & label.
"""

