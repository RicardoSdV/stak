from datetime import datetime
from time import time

from .block00_typing import *
from .block01_settings import eventLabels
from .block02_commonData import stakFlags, labelFlag
from .block04_pathOps import getStdLogPaths


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
    appendToLog((time(), stakFlags[1], datetime.now().strftime('%Y-%m-%d')))


log = Log()  # type: Log[Tup[float, str, Uni[Tup[Uni[Tup[str, int, str], Tup[Lst[str], str]], ...]]]]
appendToLog = log.append  # type: Cal[[Uni[Tup[Uni[Tup[str, int, str], Tup[Lst[str], str]], ...]]], None]
extendLog   = log.extend  # type: Cal[[Itrb[Uni[Tup[Uni[Tup[str, int, str], Tup[Lst[str], str]], ...]]]], None]
dateEntry()
