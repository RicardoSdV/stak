from datetime import datetime
from time import time

from .block00_typing import *
from .block02_settingObj import so
from .block05_pathOps import getStdLogPaths


class EventCounter(object):
    __slots__ = ('cnt',)
    def __init__(self):  # type: () -> None
        self.cnt = 0

eCnt = EventCounter()


log = []  # type: Lst[Tup[float, Uni[Tup[SplitLink, ...], str]]]
appendToLog = log.append
extendLog   = log.extend

traceLog = []  # type: Lst[Tup[float, str, SplitLink]]
appendToTrace = traceLog.append


def dateEntries():
    """ Since normal entries only log time, this one is used to log date, on logging session init & clear. """

    now = time()
    appendToLog((now, datetime.now().strftime('%Y-%m-%d')))
    # appendToTrace()  # TODO: Implement dates in trace


def labelLogs(label):
    """ Make a log entry with the passed label, else, with next label in eventLabels, if any, else print no-name label """
    if label is None:
        if eCnt.cnt < len(so.eventLabels):
            label = so.eventLabels[eCnt.cnt]
        else:
            label = 'NO-NAME LABEL' + str(len(so.eventLabels) - eCnt.cnt)

        eCnt.cnt += 1

    fmtLabel = ('\n========================================================= {} '
                '=========================================================\n'.format(label))

    now = time()
    appendToLog((now, fmtLabel))
    # appendToTrace(now, labelFlag, fmtLabel)  # TODO: Labels in trace

def clearLogs():
    """ DANGER: Clears current logs, stak, trace & std. Resets eventCnt (label print count) & more """

    for path in getStdLogPaths():
        with open(path, 'w') as _: pass

    eCnt.cnt = 0
    log[:] = []
    traceLog[:] = []
    dateEntries()



"""
What is log?

log = [
    (unixStamp, seggregatorFlag, callerFlag, theRest),
]

theRest = fileLinks OR mroLinks OR customStringEntry

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

"""
What is traceLog?

traceLog = [
]


"""

