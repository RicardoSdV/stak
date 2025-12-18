from .block00_autoImports import *

def dateEntries():
    """ Since normal entries only log time, this one is used to log date, on logging session init & clear. """

    appendToStak(
        (time(), ((None, None, None, None, (('date', DateTimeNow().strftime('%Y-%m-%d')), )), ))
    )
    # appendToTrace()  # TODO: Implement dates in trace


def labelLogs(label=None):
    """ Make a log entry with the passed label, else, with next label in eventLabels, if any, else print no-name label """
    if label is None:
        if eCnt.cnt < len(eventLabels):
            label = eventLabels[eCnt.cnt]
        else:
            label = 'NO-NAME LABEL' + str(len(eventLabels) - eCnt.cnt)

        eCnt.cnt += 1

    fmtLabel = ('\n========================================================= '
                + label + ' =========================================================\n')

    appendToStak(
        (time(), ((None, None, None, None, (('label', fmtLabel), )), ))
    )
    # appendToTrace(now, labelFlag, fmtLabel)  # TODO: Labels in trace

def clearLogs():
    """ DANGER: Clears current logs, stak, trace & std. Resets eventCnt (label print count) & more """

    eCnt.cnt = 0
    del stakLog[:]
    traceLog.clear()

    # TODO: Intern paths in logs
    # pathsByIds.clear()
    # idsByPaths.clear()

    dateEntries()


"""
What is log?

log = [
    entryID1, part1, part2, ...,
    entryID2, part1, ...
]

entryID: 32 bit signed integer = int(entryFlag, elCount)



"""




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

