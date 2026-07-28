from ..state import eCnt, stakLogExt, config, stakLog
from ..lib import timeTime, timeClock
from ..const import dateEntryFlag, labelEntryFlag

def dateEntries():
    """ CPU time is used for log entry stamps, in order to have an accurate & absolute
    stamp a reference is needed to calculate the diff from. This entry happens on logging
    session init. """

    dateEntry = (dateEntryFlag, timeTime(), timeClock())
    stakLogExt(dateEntry)
    # TODO: Implement dates in trace


def labelLogs(label=None):
    """ Make a log entry with the passed label, else, with next label in eventLabels, if any, else print no-name label """
    if label is None:
        eventLabels = config['eventLabels']

        if eCnt.cnt < len(eventLabels):
            label = eventLabels[eCnt.cnt]
        else:
            label = 'NO-NAME LABEL' + str(len(eventLabels) - eCnt.cnt)

        eCnt.cnt += 1

    fmtLabel = ('\n========================================================= '
                + label + ' =========================================================\n')

    labelEntry = (labelEntryFlag, timeClock(), fmtLabel)
    stakLogExt(labelEntry)
    # TODO: Labels in trace

def clearLogs():
    """ DANGER: Clears current logs, stak, trace & std. Resets eventCnt (label print count) & more """

    eCnt.cnt = 0
    del stakLog[:]

    # TODO: Reconsider, why are we clearing these? just let em be no?
    del splitLinksByIDs[:]
    IDsBySplitLinks.clear()

    # TODO: Tracing needs to be updated to the new flat log standard.
    # traceLog.clear()

    dateEntries()


"""
What is log?  This is outdated, but theres still some valuable info in here.

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
